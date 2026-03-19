// ============================================================
// DaPao Space Mouse — Part 7: Side Button Cap
// Curved caps that sit in the side button cutouts on the body.
// Left side = Back button, Right side = Forward button
// Print: flat side on bed, print 2 copies
// Qty: 2
// ============================================================
include <params.scad>

module side_button_cap() {
    r_at_height = shell_r(side_btn_z_frac);
    cap_w = side_btn_width - 2 * top_btn_clearance;
    cap_h = side_btn_height - 2 * top_btn_clearance;
    cap_thick = body_wall - 0.5;

    difference() {
        // Outer curved face — arc matching body curvature
        intersection() {
            translate([0, 0, 0])
                cube([cap_thick + 2, cap_w, cap_h], center=true);
            translate([-r_at_height + cap_thick/2, 0, 0])
                difference() {
                    cylinder(r=r_at_height + 0.5, h=cap_h, center=true);
                    cylinder(r=r_at_height - cap_thick, h=cap_h + 1, center=true);
                }
        }
    }

    // Inner nub (presses tactile switch)
    translate([-cap_thick/2 - 1, 0, 0])
        rotate([0, 90, 0])
            cylinder(d=top_btn_plunger_d, h=2);

    // Retention clips (top and bottom edges)
    for (z_side = [-1, 1]) {
        translate([0, 0, z_side * (cap_h/2 - 1)])
            cube([cap_thick - 0.5, cap_w * 0.3, 0.8], center=true);
    }
}

side_button_cap();
