// ============================================================
// DaPao Space Mouse — Full Parametric 3D Model  (v2)
// ============================================================
// A wireless joystick-mouse with concave cylindrical body,
// weighted base, and BLE connectivity.
//
// Button layout:
//   - Top: two half-circle rocker buttons (L/R click)
//     hinged at back, click at front — like a traditional mouse
//   - Sides: forward/back buttons on the body cylinder,
//     aligned directly below the L/R top buttons
//
// Parts:  1. Base bottom plate
//         2. Base ring (no side buttons — they moved to body)
//         3. Body shell (concave cylinder + side button cutouts)
//         4. Top frame (ring that holds the half-circle buttons)
//         5. Top button L (left half-circle rocker)
//         6. Top button R (right half-circle rocker)
//         7. Side button caps (2x, on body)
//         8. Joystick coupler
//
// Print settings: 0.2mm layer, PLA/PETG, 20% infill
// ============================================================

// --- Render Control -------------------------------------------
RENDER_PART = "assembly";
// Options: "assembly", "base_plate", "base_ring", "body",
//          "top_frame", "button_top_left", "button_top_right",
//          "button_side", "joystick_coupler"

CROSS_SECTION = false;
EXPLODE = 0;  // mm separation between parts in assembly view

// --- Global Parameters ----------------------------------------
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
// Positioned on left and right sides of the concave body,
// aligned with the L/R mouse button split (at ±90° from front)
side_btn_width    = 14;   // width along circumference (mm)
side_btn_height   = 10;   // height on body surface (mm)
side_btn_z_frac   = 0.78; // vertical position as fraction of body_height (0=bottom, 1=top)
side_btn_depth    = 2;    // how deep the button pocket is
side_btn_travel   = 1.5;  // inward click travel

// --- Top Frame & Half-Circle Buttons --------------------------
// The top frame is a ring that sits at the top of the body shell.
// Two half-circle rocker buttons sit inside the frame, split by
// a center divider. Each button hinges at the back (Y-) and
// clicks at the front (Y+).

top_frame_height  = 4;     // height of the frame ring
top_frame_wall    = 3;     // width of the outer ring
top_frame_lip     = 2;     // lip that inserts into body shell
top_frame_divider = 2;     // center divider width (between L and R)

// Half-circle button dimensions
top_btn_height    = 3;     // button shell thickness at center
top_btn_dome      = 2;     // dome rise above frame
top_btn_clearance = 0.4;   // gap between button and frame
top_btn_hinge_w   = 5;     // hinge tab width at back
top_btn_hinge_t   = 1.0;   // hinge tab thickness (living hinge — thin for flex)
top_btn_plunger_d = 3;     // switch contact nub diameter
top_btn_plunger_h = 3;     // switch contact nub height (underneath, at front)

// Switch mount posts (inside frame, front of each button)
top_sw_post_d     = 5;
top_sw_post_h     = 8;     // total height from frame bottom to switch contact point
top_sw_offset_y   = 10;    // how far forward from center the switch sits

// --- Joystick Module ------------------------------------------
joy_base_w  = 25;
joy_base_d  = 25;
joy_base_h  = 10;
joy_stick_d = 5;
joy_stick_h = 18;
joy_travel  = 18;

// --- Joystick Coupler -----------------------------------------
coupler_od      = 20;
coupler_id      = joy_stick_d + 0.4;
coupler_height  = 15;
coupler_flange  = 30;
coupler_flange_h = 3;


// ============================================================
//                     HELPER FUNCTIONS
// ============================================================

// Concave body radius at height fraction t (0=bottom, 1=top)
function shell_r(t) =
    let(
        r_top = body_od_top / 2,
        r_bot = body_od_bottom / 2,
        r_waist = body_od_waist / 2,
        r_lin = r_bot + (r_top - r_bot) * t,
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

// Half-circle (left or right). side = -1 for left, +1 for right.
// Flat edge along Y axis, curved edge is semicircle.
module half_circle(r, h, side) {
    intersection() {
        cylinder(r=r, h=h);
        if (side < 0) {
            // Left half: X <= 0
            translate([-r, -r, 0]) cube([r, 2*r, h]);
        } else {
            // Right half: X >= 0
            translate([0, -r, 0]) cube([r, 2*r, h]);
        }
    }
}


// ============================================================
//                    BASE BOTTOM PLATE
// ============================================================

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


// ============================================================
//                    BASE RING
// ============================================================
// No side button cutouts — those moved to the body shell.

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


// ============================================================
//                  CONCAVE BODY HELPERS
// ============================================================

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


// ============================================================
//                 BODY SHELL (with side button cutouts)
// ============================================================

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

        // --- Side button cutouts (left and right) ---
        // Left side button (aligned with left mouse button, at X-)
        // The cutout is a rounded rectangle punched through the shell wall
        translate([0, 0, side_btn_z])
            rotate([0, 0, 90])  // rotate to left side (X- direction)
                side_button_cutout();

        // Right side button (aligned with right mouse button, at X+)
        translate([0, 0, side_btn_z])
            rotate([0, 0, -90])  // rotate to right side (X+ direction)
                side_button_cutout();
    }
}

// Punches a rounded-rect hole through the concave wall at the current Z height
// Oriented to cut through the wall along the local X+ direction
module side_button_cutout() {
    // We need to cut from outside to inside through the curved wall
    // The shell radius at this height:
    r_at_height = shell_r(side_btn_z_frac);
    cut_depth = body_wall + 4;  // generous cut-through

    translate([r_at_height - cut_depth/2, 0, 0])
        rotate([0, 0, 0])
            rounded_rect(cut_depth, side_btn_width, side_btn_height, 2);
}


// ============================================================
//               TOP FRAME (ring + divider)
// ============================================================
// Sits at the top of the body. Has an outer ring, a center
// divider, and the two half-circle buttons sit inside it.

module top_frame() {
    frame_od = body_od_top;
    frame_id = frame_od - 2 * top_frame_wall;
    btn_r = frame_id / 2 - top_btn_clearance;

    difference() {
        union() {
            // Outer ring
            difference() {
                cylinder(d=frame_od, h=top_frame_height);
                translate([0, 0, -0.1])
                    cylinder(d=frame_id, h=top_frame_height + 0.2);
            }

            // Center divider (runs front to back along Y axis)
            translate([-top_frame_divider/2, -frame_od/2, 0])
                cube([top_frame_divider, frame_od, top_frame_height]);

            // Insertion lip (goes into body shell)
            translate([0, 0, -top_frame_lip])
                difference() {
                    cylinder(d=body_od_top - 2*body_wall - tol, h=top_frame_lip);
                    translate([0, 0, -0.1])
                        cylinder(d=body_od_top - 2*body_wall - tol - 4, h=top_frame_lip + 0.2);
                }

            // Switch mount posts (underneath, at front of each button half)
            // Left switch post
            translate([-frame_id/4, top_sw_offset_y, -top_sw_post_h])
                cylinder(d=top_sw_post_d, h=top_sw_post_h);
            // Right switch post
            translate([frame_id/4, top_sw_offset_y, -top_sw_post_h])
                cylinder(d=top_sw_post_d, h=top_sw_post_h);

            // Hinge shelves at back (Y-) for button pivot points
            // Left hinge shelf
            translate([-frame_id/4, -(frame_id/2 - 2), 0])
                cube([top_btn_hinge_w + 2, 4, top_frame_height], center=true);
            // Right hinge shelf
            translate([frame_id/4, -(frame_id/2 - 2), 0])
                cube([top_btn_hinge_w + 2, 4, top_frame_height], center=true);
        }

        // Trim divider and hinge shelves to cylinder boundary
        difference() {
            cylinder(d=frame_od + 10, h=100, center=true);
            cylinder(d=frame_od, h=101, center=true);
        }

        // Switch screw holes in posts
        translate([-frame_id/4, top_sw_offset_y, -top_sw_post_h - 0.1])
            cylinder(d=pcb_screw_d, h=top_sw_post_h + 0.2);
        translate([frame_id/4, top_sw_offset_y, -top_sw_post_h - 0.1])
            cylinder(d=pcb_screw_d, h=top_sw_post_h + 0.2);
    }
}


// ============================================================
//            TOP BUTTON (half-circle rocker)
// ============================================================
// side: -1 = left, +1 = right
// Hinges at back (Y-), clicks at front (Y+)
// Shaped as a half-circle dome that matches the body diameter

module top_button(side) {
    frame_id = body_od_top - 2 * top_frame_wall;
    btn_r = frame_id / 2 - top_btn_clearance;

    difference() {
        union() {
            // Half-circle button body
            intersection() {
                // Full button disc with dome
                difference() {
                    // Domed top surface
                    translate([0, 0, 0])
                        scale([1, 1, (top_btn_height + top_btn_dome) / btn_r])
                            sphere(r=btn_r);
                    // Hollow underneath (save material, leave shell)
                    translate([0, 0, -btn_r])
                        scale([1, 1, (top_btn_height + top_btn_dome) / btn_r])
                            sphere(r=btn_r - 1.5);
                    // Cut off bottom hemisphere
                    translate([0, 0, -btn_r])
                        cube([2*btn_r, 2*btn_r, 2*btn_r], center=true);
                }

                // Trim to half-circle (left or right)
                if (side < 0) {
                    // Left: keep X < -clearance/2
                    translate([-(btn_r + 1), -(btn_r + 1), -1])
                        cube([btn_r + 1 - top_frame_divider/2 - top_btn_clearance/2,
                              2*(btn_r + 1),
                              top_btn_height + top_btn_dome + 2]);
                } else {
                    // Right: keep X > clearance/2
                    translate([top_frame_divider/2 + top_btn_clearance/2, -(btn_r + 1), -1])
                        cube([btn_r + 1 - top_frame_divider/2 - top_btn_clearance/2,
                              2*(btn_r + 1),
                              top_btn_height + top_btn_dome + 2]);
                }

                // Also trim to within frame_id circle
                cylinder(r=btn_r, h=top_btn_height + top_btn_dome + 2);
            }

            // Hinge tab at back (Y-)
            // A thin flexible strip connecting button to frame at the back
            translate([side * frame_id/4, -(btn_r - top_btn_hinge_w/2), 0])
                cube([top_btn_hinge_w, top_btn_hinge_w, top_btn_hinge_t], center=false);
        }
    }

    // Switch plunger contact (underneath, at front of button)
    translate([side * frame_id/4, top_sw_offset_y, -top_btn_plunger_h])
        cylinder(d=top_btn_plunger_d, h=top_btn_plunger_h);
}


// ============================================================
//              SIDE BUTTON CAP (for body cutouts)
// ============================================================
// Curved caps that sit in the side button cutouts on the body.
// The outer face follows the concave body curve.

module side_button_cap() {
    r_at_height = shell_r(side_btn_z_frac);
    cap_w = side_btn_width - 2 * top_btn_clearance;
    cap_h = side_btn_height - 2 * top_btn_clearance;
    cap_thick = body_wall - 0.5;  // slightly thinner than wall

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

    // Retention clips (small bumps on top and bottom edges to keep cap in place)
    for (z_side = [-1, 1]) {
        translate([0, 0, z_side * (cap_h/2 - 1)])
            cube([cap_thick - 0.5, cap_w * 0.3, 0.8], center=true);
    }
}


// ============================================================
//                   JOYSTICK COUPLER
// ============================================================

module joystick_coupler() {
    difference() {
        union() {
            cylinder(d=coupler_od, h=coupler_height);
            translate([0, 0, coupler_height - coupler_flange_h])
                cylinder(d=coupler_flange, h=coupler_flange_h);
        }

        // Bore
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


// ============================================================
//              JOYSTICK MODULE (ghost reference)
// ============================================================

module joystick_module_ref() {
    color("dimgray", 0.5) {
        translate([-joy_base_w/2, -joy_base_d/2, 0])
            cube([joy_base_w, joy_base_d, joy_base_h]);
        cylinder(d=joy_stick_d, h=joy_base_h + joy_stick_h);
        translate([0, 0, joy_base_h + joy_stick_h])
            sphere(d=joy_stick_d + 2);
    }
}


// ============================================================
//                       ASSEMBLY
// ============================================================

module assembly() {
    e = EXPLODE;
    body_z = plate_thick + base_height + tilt_clearance;
    top_z  = body_z + body_height;
    side_btn_z = body_z + body_height * side_btn_z_frac;

    // Base plate
    color("SlateGray")
        translate([0, 0, -e])
            base_plate();

    // Base ring
    color("SteelBlue")
        translate([0, 0, plate_thick])
            base_ring();

    // Joystick module (ghost)
    translate([0, 0, plate_thick + base_floor])
        joystick_module_ref();

    // Joystick coupler
    color("Orange")
        translate([0, 0, plate_thick + base_floor + joy_base_h + joy_stick_h - coupler_height + e*0.5])
            joystick_coupler();

    // Body shell
    color("DodgerBlue", 0.85)
        translate([0, 0, body_z + e])
            body_shell();

    // Top frame
    color("SteelBlue")
        translate([0, 0, top_z + e*2])
            top_frame();

    // Top button — Left (half-circle rocker)
    color("White", 0.92)
        translate([0, 0, top_z + top_frame_height + e*2.5])
            top_button(-1);

    // Top button — Right (half-circle rocker)
    color("WhiteSmoke", 0.92)
        translate([0, 0, top_z + top_frame_height + e*2.5])
            top_button(1);

    // Side button — Left (back button)
    color("LightGray", 0.9)
        translate([0, 0, side_btn_z + e])
            rotate([0, 0, 90])
                translate([shell_r(side_btn_z_frac) - body_wall/2, 0, 0])
                    side_button_cap();

    // Side button — Right (forward button)
    color("LightGray", 0.9)
        translate([0, 0, side_btn_z + e])
            rotate([0, 0, -90])
                translate([shell_r(side_btn_z_frac) - body_wall/2, 0, 0])
                    side_button_cap();
}


// ============================================================
//                    RENDER DISPATCH
// ============================================================

if (RENDER_PART == "assembly") {
    if (CROSS_SECTION) {
        difference() {
            assembly();
            translate([0, -200, -10]) cube([200, 400, 200]);
        }
    } else {
        assembly();
    }
}
else if (RENDER_PART == "base_plate") {
    base_plate();
}
else if (RENDER_PART == "base_ring") {
    base_ring();
}
else if (RENDER_PART == "body") {
    body_shell();
}
else if (RENDER_PART == "top_frame") {
    top_frame();
}
else if (RENDER_PART == "button_top_left") {
    top_button(-1);
}
else if (RENDER_PART == "button_top_right") {
    top_button(1);
}
else if (RENDER_PART == "button_side") {
    side_button_cap();
}
else if (RENDER_PART == "joystick_coupler") {
    joystick_coupler();
}
else {
    echo("Unknown RENDER_PART. Options: assembly, base_plate, base_ring, body, top_frame, button_top_left, button_top_right, button_side, joystick_coupler");
}
