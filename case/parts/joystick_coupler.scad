// ============================================================
// DaPao Space Mouse — Part 8: Joystick Coupler (v2)
// Connects joystick stick to body shell coupler seat.
// Fix: weight-reduction pocket now properly bounded so it can't
//      punch through the outer wall or the bore.
// Print: upright, flange on top, no supports.
// Qty: 1
// ============================================================
include <params.scad>

module joystick_coupler() {
    difference() {
        union() {
            // Main shaft
            cylinder(d = coupler_od, h = coupler_height);
            // Flange at top — seats into body shell coupler pocket
            translate([0, 0, coupler_height - coupler_flange_h])
                cylinder(d = coupler_flange, h = coupler_flange_h);
        }

        // Central bore for joystick stick
        translate([0, 0, -0.1])
            cylinder(d = coupler_id, h = coupler_height + 0.2);

        // Set screw hole (M2) — tapped after printing
        translate([0, 0, coupler_height * 0.35])
            rotate([90, 0, 0])
                cylinder(d = 2, h = coupler_od + 0.2, center = true);

        // Weight reduction pocket — safely bounded between bore and outer wall
        // Only in the lower half, clear of the flange
        pocket_r_outer = coupler_od / 2 - 2;
        pocket_r_inner = coupler_id / 2 + 1.5;
        pocket_h       = coupler_height * 0.45 - 2;
        if (pocket_r_outer > pocket_r_inner + 1) {
            translate([0, 0, 2])
                difference() {
                    cylinder(r = pocket_r_outer, h = pocket_h);
                    cylinder(r = pocket_r_inner, h = pocket_h + 0.2);
                }
        }
    }
}

joystick_coupler();
