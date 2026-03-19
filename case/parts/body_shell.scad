// ============================================================
// DaPao Space Mouse — Part 3: Concave Body Shell
// Contains: hourglass body with side button cutouts,
//           internal coupler mounting ring, top frame socket
// Print: upright, supports for side button cutout overhangs
// Qty: 1
// ============================================================
include <params.scad>

module body_concave_solid(inset) {
    n = body_resolution;
    step = body_height / n;
    for (i = [0:n-1]) {
        t1 = i / n;
        t2 = (i + 1) / n;
        r1 = shell_r(t1) - inset;
        r2 = shell_r(t2) - inset;
        z1 = i * step;
        z2 = (i + 1) * step;
        hull() {
            translate([0, 0, z1]) cylinder(r=max(r1, 1), h=0.01);
            translate([0, 0, z2]) cylinder(r=max(r2, 1), h=0.01);
        }
    }
}

// Punches a rounded-rect hole through the concave wall at the current Z height
module side_button_cutout() {
    r_at_height = shell_r(side_btn_z_frac);
    cut_depth = body_wall + 4;
    translate([r_at_height - cut_depth/2, 0, 0])
        rounded_rect(cut_depth, side_btn_width, side_btn_height, 2);
}

module body_shell() {
    side_btn_z = body_height * side_btn_z_frac;

    difference() {
        union() {
            // Outer concave surface minus inner cavity
            difference() {
                body_concave_solid(0);
                translate([0, 0, -0.1])
                    body_concave_solid(body_wall);
            }

            // Internal mounting ring at bottom for joystick coupler
            difference() {
                cylinder(d=coupler_flange + 4, h=3);
                translate([0, 0, -0.1])
                    cylinder(d=coupler_od + tol, h=3.2);
            }
        }

        // Hollow out top for top frame insertion
        translate([0, 0, body_height - top_frame_lip - 0.1])
            cylinder(d=body_od_top - 2*body_wall + tol, h=top_frame_lip + 0.2);

        // Side button cutout — Left (X-)
        translate([0, 0, side_btn_z])
            rotate([0, 0, 90])
                side_button_cutout();

        // Side button cutout — Right (X+)
        translate([0, 0, side_btn_z])
            rotate([0, 0, -90])
                side_button_cutout();
    }
}

body_shell();
