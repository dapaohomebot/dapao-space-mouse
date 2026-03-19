// ============================================================
// DaPao Space Mouse — Part 8: Joystick Coupler
// Connects the joystick stick to the body shell.
// Flange seats into the mounting ring at the bottom of body_shell.
// Print: upright, flange on top, no supports needed
// Qty: 1
// ============================================================
include <params.scad>

module joystick_coupler() {
    difference() {
        union() {
            cylinder(d=coupler_od, h=coupler_height);
            translate([0, 0, coupler_height - coupler_flange_h])
                cylinder(d=coupler_flange, h=coupler_flange_h);
        }

        // Bore (joystick stick passes through)
        translate([0, 0, -0.1])
            cylinder(d=coupler_id, h=coupler_height + 0.2);

        // Set screw hole
        translate([0, 0, coupler_height * 0.4])
            rotate([90, 0, 0])
                cylinder(d=2, h=coupler_od, center=true);

        // Weight reduction
        translate([0, 0, coupler_height * 0.5])
            difference() {
                cylinder(d=coupler_od - 4, h=coupler_height * 0.5 - coupler_flange_h);
                cylinder(d=coupler_id + 4, h=coupler_height);
            }
    }
}

joystick_coupler();
