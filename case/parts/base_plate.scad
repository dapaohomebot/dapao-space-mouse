// ============================================================
// DaPao Space Mouse — Part 1: Base Bottom Plate
// Print: flat side down, no supports needed
// Qty: 1
// ============================================================
include <params.scad>

module base_plate() {
    difference() {
        union() {
            cylinder(d=base_od, h=plate_thick);
            for (i = [0:assy_screw_count-1]) {
                angle = i * 360 / assy_screw_count + 45;
                translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), 0])
                    cylinder(d=6, h=plate_thick);
            }
        }

        // Steel insert pockets
        for (i = [0:steel_pocket_count-1]) {
            angle = i * 360 / steel_pocket_count;
            translate([steel_pocket_r * cos(angle), steel_pocket_r * sin(angle), -0.1])
                cylinder(d=steel_pocket_d, h=steel_pocket_depth + 0.1);
        }

        // Rubber foot recesses
        for (i = [0:3]) {
            angle = i * 90 + 45;
            r = base_od/2 - foot_d/2 - 2;
            translate([r * cos(angle), r * sin(angle), -0.1])
                cylinder(d=foot_d, h=foot_depth + 0.1);
        }

        // Assembly screw holes
        for (i = [0:assy_screw_count-1]) {
            angle = i * 360 / assy_screw_count + 45;
            translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), -0.1])
                cylinder(d=assy_screw_d, h=plate_thick + 0.2);
        }

        // Center hole
        translate([0, 0, -0.1])
            cylinder(d=joy_base_w + 4, h=plate_thick + 0.2);
    }
}

base_plate();
