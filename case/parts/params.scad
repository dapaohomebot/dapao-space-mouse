// ============================================================
// DaPao Space Mouse — Shared Parameters & Utilities
// Include this file in all part files: include <params.scad>
// ============================================================

$fn = 80;

// Tolerances
tol        = 0.3;
print_tol  = 0.15;

// --- Base Dimensions ------------------------------------------
base_od       = 100;
base_id       = 94;
base_height   = 25;
base_wall     = 3;
base_floor    = 2;

plate_thick       = 3;
plate_screw_inset = 8;

// Steel insert pockets
steel_pocket_d     = 22;
steel_pocket_depth = 8;
steel_pocket_r     = 35;
steel_pocket_count = 4;

// USB-C port
usbc_width  = 9.5;
usbc_height = 3.5;
usbc_z      = 8;

// PCB mounting
pcb_standoff_h   = 5;
pcb_standoff_d   = 5;
pcb_screw_d      = 1.8;
pcb_mount_spread = 30;

// Rubber feet
foot_d     = 10;
foot_depth = 1;

// Assembly screws
assy_screw_d     = 2.2;
assy_screw_count = 4;
assy_screw_r     = 44;

// Power switch
sw_width  = 7;
sw_height = 4;
sw_z      = 18;
sw_angle  = 180;

// --- Body Dimensions ------------------------------------------
body_od_top      = 60;
body_od_bottom   = 60;
body_od_waist    = 44;
body_height      = 55;
body_wall        = 2.5;
body_waist_pos   = 0.45;
body_resolution  = 60;

tilt_clearance   = 6;
tilt_angle_max   = 18;

// --- Side Buttons (on body) -----------------------------------
side_btn_width    = 14;
side_btn_height   = 10;
side_btn_z_frac   = 0.82;  // center at 45mm — cutout spans 40-50mm, clear of 53mm top socket
side_btn_depth    = 2;
side_btn_travel   = 1.5;

// --- Top Frame & Half-Circle Buttons --------------------------
top_frame_height  = 4;
top_frame_wall    = 3;
top_frame_lip     = 2;
top_frame_divider = 2;

top_btn_height    = 3;
top_btn_dome      = 2;
top_btn_clearance = 0.4;
top_btn_hinge_w   = 5;
top_btn_hinge_t   = 1.0;
top_btn_plunger_d = 3;
top_btn_plunger_h = 3;

top_sw_post_d     = 5;
top_sw_post_h     = 8;
top_sw_offset_y   = 12;   // Y distance from center to L/R switch (matches PCB SW4/SW5)
top_sw_x          = 10;   // X distance from center to L/R switch (matches PCB SW4/SW5)
top_mount_x       = 15;   // X distance from center to PCB M2 mount holes (matches PCB H1/H2)
top_mount_y       = 0;    // Y distance from center to PCB M2 mount holes

// Top frame side switch cutouts (for SW6 Back / SW7 Fwd on upper PCB)
top_side_sw_w     = 9;    // cutout width through frame wall
top_side_sw_h     = 5;    // cutout height through frame wall

// --- Joystick Module ------------------------------------------
joy_base_w  = 25;
joy_base_d  = 25;
joy_base_h  = 10;
joy_stick_d = 5;
joy_stick_h = 18;
joy_travel  = 18;

// --- Joystick Coupler -----------------------------------------
coupler_od       = 20;
coupler_id       = joy_stick_d + 0.4;
coupler_height   = 15;
coupler_flange   = 30;
coupler_flange_h = 3;


// ============================================================
//                     HELPER FUNCTIONS
// ============================================================

// Concave body radius at height fraction t (0=bottom, 1=top)
function shell_r(t) =
    let(
        r_top    = body_od_top / 2,
        r_bot    = body_od_bottom / 2,
        r_waist  = body_od_waist / 2,
        r_lin    = r_bot + (r_top - r_bot) * t,
        envelope = sin(t * 180),
        max_depth = (r_bot + r_top)/2 - r_waist
    )
    r_lin - max_depth * pow(envelope, 1.3);


// ============================================================
//                     UTILITY MODULES
// ============================================================

module rounded_rect(w, l, h, r) {
    translate([0, 0, h/2])
        hull() {
            for (x = [-1, 1], y = [-1, 1])
                translate([x*(w/2-r), y*(l/2-r), 0])
                    cylinder(r=r, h=h, center=true);
        }
}

module rounded_slot(w, h, depth) {
    r = h / 2;
    hull() {
        translate([0, -(w/2 - r), 0]) cylinder(r=r, h=depth);
        translate([0,  (w/2 - r), 0]) cylinder(r=r, h=depth);
    }
}

module half_circle(r, h, side) {
    intersection() {
        cylinder(r=r, h=h);
        if (side < 0) {
            translate([-r, -r, 0]) cube([r, 2*r, h]);
        } else {
            translate([0, -r, 0]) cube([r, 2*r, h]);
        }
    }
}
