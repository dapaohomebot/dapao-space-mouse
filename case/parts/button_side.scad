// ============================================================
// DaPao Space Mouse — Part 7: Side Button Cap (v2)
// Curved cap fitting the body shell side cutouts.
// Fix: simplified to a solid curved block — no floating shell slivers.
// Fix: retention clips are now part of the solid block, not separate.
// Print: flat (inner) face down, print 2 copies.
// Qty: 2
// ============================================================
include <params.scad>

module side_button_cap() {
    r_at_height = shell_r(side_btn_z_frac);  // body outer radius at button height
    cap_w       = side_btn_width  - 2 * top_btn_clearance;
    cap_h       = side_btn_height - 2 * top_btn_clearance;
    cap_thick   = body_wall - 0.3;  // slightly thinner than wall for fit

    // Solid curved block matching body outer curvature
    intersection() {
        // Bounding box
        translate([-cap_thick / 2, -cap_w / 2, -cap_h / 2])
            cube([cap_thick, cap_w, cap_h]);

        // Cylindrical arc (outer face follows body curve)
        cylinder(r = r_at_height, h = cap_h, center = true);
    }

    // Retention nubs on top and bottom edges — keep cap seated in cutout
    for (z_s = [-1, 1]) {
        translate([0, 0, z_s * (cap_h / 2)])
            intersection() {
                translate([-cap_thick / 2, -cap_w * 0.2, 0])
                    cube([cap_thick, cap_w * 0.4, 1.2]);
                cylinder(r = r_at_height + 0.1, h = 1.2, center = true);
            }
    }

    // Inner nub — presses tactile switch mounted inside body
    // Protrudes inward (negative X from body outer surface)
    translate([-(r_at_height - cap_thick / 2), 0, 0])
        rotate([0, -90, 0])
            cylinder(d = top_btn_plunger_d, h = 2.5);
}

side_button_cap();
