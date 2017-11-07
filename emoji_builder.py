def main(argv):
    import glob
    from fontTools import ttx, ttLib

    options = []

    option_map = {
        "-V": "verbose",
        "-O": "keep_outlines",
        "-U": "uncompressed",
        "-C": "keep_chunks",
    }

    for key, value in option_map.items():
        if key in argv:
            options.append(value)
            argv.remove(key)

    if len(argv) < 4:
        print >> sys.stderr, """
Usage:

emoji_builder.py [-V] [-O] [-U] [-A] font.ttf out-font.ttf strike-prefix...

This will search for files that have strike-prefix followed
by a hex number, and end in ".png".  For example, if strike-prefix
is "icons/uni", then files with names like "icons/uni1f4A9.png" will
be loaded.  All images for the same strike should have the same size
for best results.

If multiple strike-prefix parameters are provided, multiple
strikes will be embedded, in the order provided.

The script then embeds color bitmaps in the font, for characters
that the font already supports, and writes the new font out.

If -V is given, verbose mode is enabled.

If -U is given, uncompressed images are stored (imageFormat=1).
By default, PNG images are stored (imageFormat=17).

If -O is given, the outline tables ('glyf', 'CFF ') and
related tables are NOT dropped from the font.
By default they are dropped.

If -C is given, unused chunks (color profile, etc) are NOT
dropped from the PNG images when embedding.
By default they are dropped.
"""
        sys.exit(1)

    font_file = argv[1]
    out_file = argv[2]
    img_prefixes = argv[3:]
    del argv

    def add_font_table(font, tag, data):
        tab = ttLib.tables.DefaultTable.DefaultTable(tag)
        tab.data = str(data)
        font[tag] = tab

    def drop_outline_tables(font):
        for tag in ['cvt ', 'fpgm', 'glyf', 'loca', 'prep', 'CFF ', 'VORG']:
            try:
                del font[tag]
            except KeyError:
                pass

    print

    font = ttx.TTFont(font_file)
    print "Loaded font '%s'." % font_file

    font_metrics = FontMetrics(font['head'].unitsPerEm,
                               font['hhea'].ascent,
                               -font['hhea'].descent)
    print "Font metrics: upem=%d ascent=%d descent=%d." % \
          (font_metrics.upem, font_metrics.ascent, font_metrics.descent)
    glyph_metrics = font['hmtx'].metrics
    unicode_cmap = font['cmap'].getcmap(3, 10)
    if not unicode_cmap:
        unicode_cmap = font['cmap'].getcmap(3, 1)
    if not unicode_cmap:
        raise Exception("Failed to find a Unicode cmap.")

    image_format = 1 if 'uncompressed' in options else 17

    ebdt = CBDT(font_metrics, options)
    ebdt.write_header()
    eblc = CBLC(font_metrics, options)
    eblc.write_header()
    eblc.start_strikes(len(img_prefixes))

    for img_prefix in img_prefixes:

        print

        img_files = {}
        glb = "%s*.png" % img_prefix
        print "Looking for images matching '%s'." % glb
        for img_file in glob.glob(glb):
            uchar = int(img_file[len(img_prefix):-4], 16)
            img_files[uchar] = img_file
        if not img_files:
            raise Exception("No image files found in '%s'." % glb)
        print "Found images for %d characters in '%s'." % (len(img_files), glb)

        glyph_imgs = {}
        advance = width = height = 0
        for uchar, img_file in img_files.items():
            if uchar in unicode_cmap.cmap:
                glyph_name = unicode_cmap.cmap[uchar]
                glyph_id = font.getGlyphID(glyph_name)
                glyph_imgs[glyph_id] = img_file
                if "verbose" in options:
                    print "Matched U+%04X: id=%d name=%s image=%s" % (uchar, glyph_id, glyph_name, img_file)

                advance += glyph_metrics[glyph_name][0]
                w, h = PNG(img_file).get_size()
                width += w
                height += h

        glyphs = sorted(glyph_imgs.keys())
        if not glyphs:
            raise Exception("No common characteres found between font and '%s'." % glb)
        print "Embedding images for %d glyphs for this strike." % len(glyphs)

        advance, width, height = (div(x, len(glyphs)) for x in (advance, width, height))
        strike_metrics = StrikeMetrics(font_metrics, advance, width, height)
        print "Strike ppem set to %d." % (strike_metrics.y_ppem)

        ebdt.start_strike(strike_metrics)
        ebdt.write_glyphs(glyphs, glyph_imgs, image_format)
        glyph_maps = ebdt.end_strike()

        eblc.write_strike(strike_metrics, glyph_maps)

    print

    ebdt = ebdt.data()
    add_font_table(font, 'CBDT', ebdt)
    print "CBDT table synthesized: %d bytes." % len(ebdt)
    eblc.end_strikes()
    eblc = eblc.data()
    add_font_table(font, 'CBLC', eblc)
    print "CBLC table synthesized: %d bytes." % len(eblc)

    print

    if 'keep_outlines' not in options:
        drop_outline_tables(font)
        print "Dropped outline ('glyf', 'CFF ') and related tables."

    font.save(out_file)
    print "Output font '%s' generated." % out_file
