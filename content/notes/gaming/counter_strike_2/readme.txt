CS2 spray pattern trainer notes

spray_patterns.json contains the spray pattern data used by spray_pattern_trainer.html.

How the current data was extracted
----------------------------------

We first tried to derive spray patterns from weapons.vdata, but the weapon file does
not appear to contain the final fixed spray paths directly. It has useful weapon
settings such as fire rate, clip size, recoil magnitude, recoil angle, and seeds,
but our generated paths from those values did not match the known in-game spray
patterns. For example, the AK-47 pattern should climb and then sweep sideways,
while the weapons.vdata-derived guess did not reproduce that behavior accurately.

The current extractor, extract_spray_patterns.py, decodes the data from OP.GG's
CS2 spray pattern page. The page ships an encoded client payload. The script
fetches the page, extracts the React Flight text record that contains the encoded
patterns, base64-decodes it, XOR-decodes it with the key used by the client, and
writes the result into spray_patterns.json in the format used by the local trainer.

Updating the data in the future
-------------------------------

If the spray patterns change and OP.GG is no longer a suitable source, the most
reliable path is probably to extract the data from the game empirically:

1. Load each weapon in CS2.
2. Shoot a full magazine at a flat wall from a fixed position.
3. Record or screenshot the bullet impacts.
4. Extract the bullet impact centers in order.
5. Normalize those coordinates into the trainer's pattern format.

That is slower than reading a weapon config file, but it matches what the trainer
actually needs: the final observed bullet path, not just the recoil parameters that
contribute to it.

Coordinate scale
----------------

Do not independently normalize each weapon to fill the canvas. The relative size
of each spray pattern is meaningful: a larger spray should remain larger than a
smaller spray. The trainer should compute one shared scale across the full weapon
dataset and use that scale for every weapon. Individual patterns can still be
centered on the canvas for readability, but their zoom level should stay uniform.

The pattern scale control is a user display multiplier on top of that shared
scale. Its default is 0.5, and it should shrink or grow every weapon together
without making each weapon independently fit the canvas.
