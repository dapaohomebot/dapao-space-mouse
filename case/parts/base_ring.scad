// ============================================================
// DaPao Space Mouse — Part 2: Base Ring
// Contains: PCB mounts, USB-C cutout, power switch cutout,
//           battery compartment, joystick clearance
// Print: upright, supports for USB-C overhang
// Qty: 1
// ============================================================
include <params.scad>

module base_ring() {
    difference() {
        union() {
            // Outer wall
            difference() {
                cylinder(d=base_od, h=base_height);
                translate([0, 0, base_floor])
                    cylinder(d=base_od - 2*base_wall, h=base_height);
            }

            // Floor
            cylinder(d=base_od, h=base_floor);

            // PCB standoffs
            for (i = [0:3]) {
                angle = i * 90;
                translate([pcb_mount_spread * cos(angle), pcb_mount_spread * sin(angle), base_floor])
                    cylinder(d=pcb_standoff_d, h=pcb_standoff_h);
            }

            // Joystick mount pad
            translate([0, 0, base_floor])
                cylinder(d=joy_base_w + 8, h=3);

            // Screw bosses
            for (i = [0:assy_screw_count-1]) {
                angle = i * 360 / assy_screw_count + 45;
                translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), 0])
                    cylinder(d=6, h=base_height);
            }
        }

        // PCB screw holes
        for (i = [0:3]) {
            angle = i * 90;
            translate([pcb_mount_spread * cos(angle), pcb_mount_spread * sin(angle), base_floor - 0.1])
                cylinder(d=pcb_screw_d, h=pcb_standoff_h + 0.2);
        }

        // Joystick clearance
        translate([0, 0, -0.1])
            cylinder(d=joy_base_w + 2, h=base_floor + 4);
        translate([0, 0, -0.1])
            cylinder(d=joy_stick_d + 10, h=base_height + 0.2);

        // USB-C port cutout (back)
        translate([base_od/2 - base_wall - 1, 0, usbc_z])
            rotate([0, 90, 0])
                rounded_slot(usbc_width, usbc_height, base_wall + 2);

        // Power switch cutout (opposite from USB)
        rotate([0, 0, sw_angle])
            translate([base_od/2 - base_wall - 1, 0, sw_z])
                rotate([0, 90, 0])
                    rounded_slot(sw_width, sw_height, base_wall + 2);

        // Assembly screw holes
        for (i = [0:assy_screw_count-1]) {
            angle = i * 360 / assy_screw_count + 45;
            translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), -0.1])
                cylinder(d=assy_screw_d, h=base_height + 0.2);
        }

        // Battery compartment clearance
        translate([20, 0, base_floor + 0.1])
            cube([30, 40, 12], center=true);
    }
}

base_ring();
