// ============================================================
// DaPao Space Mouse — Full Parametric 3D Model
// ============================================================
// A wireless joystick-mouse with concave cylindrical body,
// weighted base, and BLE connectivity.
//
// Parts:  1. Base bottom plate
//         2. Base ring
//         3. Body shell (concave cylinder)
//         4. Top cap (with button cutouts)
//         5. Button caps (2 top + 2 side)
//         6. Joystick coupler
//
// Print settings: 0.2mm layer, PLA/PETG, 20% infill
// ============================================================

// --- Render Control -------------------------------------------
// Set to the part you want to render/export, or "assembly" to preview all
// Options: "assembly", "base_plate", "base_ring", "body", "top_cap",
//          "button_top_left", "button_top_right", "button_side",
//          "joystick_coupler"
RENDER_PART = "assembly";

// Show cross-section in assembly view (for inspection)
CROSS_SECTION = false;

// Explode assembly for visualization (mm of separation)
EXPLODE = 0; // set to e.g. 15 to separate parts

// --- Global Parameters ----------------------------------------
$fn = 80;               // circle resolution (increase for final render)

// Tolerances
tol        = 0.3;       // general clearance between mating parts
print_tol  = 0.15;      // press-fit tolerance

// --- Base Dimensions ------------------------------------------
base_od       = 100;    // outer diameter
base_id       = 94;     // inner diameter (wall = 3mm)
base_height   = 25;     // total base ring height
base_wall     = 3;      // wall thickness
base_floor    = 2;      // bottom plate thickness

// Base plate
plate_thick   = 3;      // bottom plate thickness
plate_screw_inset = 8;  // screw hole distance from edge

// Steel insert pockets (for weight)
steel_pocket_d     = 22;  // pocket diameter (fits M10 washers ~20mm OD)
steel_pocket_depth = 8;   // pocket depth (stack 3-4 washers)
steel_pocket_r     = 35;  // distance from center to pocket center
steel_pocket_count = 4;   // number of pockets

// USB-C port
usbc_width  = 9.5;      // USB-C connector width
usbc_height = 3.5;      // USB-C connector height
usbc_z      = 8;        // height of port center from base bottom

// Side buttons
side_btn_width   = 12;  // button opening width
side_btn_height  = 8;   // button opening height
side_btn_z       = 14;  // center height from base bottom
side_btn_angle   = 90;  // degrees from USB-C port (left/right)

// PCB mounting
pcb_standoff_h   = 5;   // standoff height from base floor
pcb_standoff_d   = 5;   // standoff outer diameter
pcb_screw_d      = 1.8; // M2 screw hole (slightly under for self-tap)
pcb_mount_spread = 30;  // distance from center to standoff

// Rubber feet
foot_d     = 10;        // foot pad diameter
foot_depth = 1;         // recess depth for adhesive pad

// Assembly screws (base plate to ring)
assy_screw_d     = 2.2;  // M2 clearance
assy_screw_count = 4;
assy_screw_r     = 44;   // distance from center

// --- Body Dimensions ------------------------------------------
body_od_top      = 60;   // diameter at top and bottom edges
body_od_bottom   = 60;
body_od_waist    = 44;   // diameter at narrowest point (concave)
body_height      = 55;   // total body shell height
body_wall        = 2.5;  // wall thickness
body_waist_pos   = 0.45; // waist position (0-1, fraction of height)
body_resolution  = 60;   // number of vertical slices for concave profile

// Clearance ring (gap between body bottom and base top for tilt)
tilt_clearance   = 6;    // mm gap at rest for tilt freedom
tilt_angle_max   = 18;   // max tilt angle in degrees

// --- Top Cap Dimensions ---------------------------------------
top_cap_height   = 10;    // total height of top cap
top_cap_lip      = 2;     // internal lip depth that fits inside body
top_cap_wall     = 2.5;

// Top button cutouts
top_btn_width    = 14;    // button opening width
top_btn_length   = 20;    // button opening length (front to back)
top_btn_spacing  = 6;     // gap between left and right buttons
top_btn_offset_y = 5;     // offset toward front from center
top_btn_depth    = 6;     // button travel well depth

// --- Button Cap Dimensions ------------------------------------
btn_cap_clearance = 0.25; // clearance around button cap
btn_cap_height    = 4;    // how tall the cap sticks up
btn_cap_thickness = 2;    // cap plate thickness
btn_cap_hinge_w   = 2;    // living hinge width (for top buttons)

// Side button cap
side_btn_cap_thick = 2;

// --- Joystick Module (reference for mounting) -----------------
// Models a generic Alps RKJXV-style joystick
joy_base_w  = 25;       // module base width
joy_base_d  = 25;       // module base depth
joy_base_h  = 10;       // module base height
joy_stick_d = 5;        // stick diameter
joy_stick_h = 18;       // stick height above base
joy_travel  = 18;       // max tilt at tip

// --- Joystick Coupler -----------------------------------------
coupler_od      = 20;    // outer diameter
coupler_id      = joy_stick_d + 0.4; // inner bore (fits joystick stick)
coupler_height  = 15;    // total height
coupler_flange  = 30;    // flange diameter (connects to body shell)
coupler_flange_h = 3;    // flange thickness

// --- Power Switch Cutout --------------------------------------
sw_width  = 7;
sw_height = 4;
sw_z      = 18;          // height from base bottom
sw_angle  = 180;         // opposite side from USB-C

// ============================================================
//                        MODULES
// ============================================================

// --- Concave Profile Generator --------------------------------
// Returns the radius at a given height fraction (0=bottom, 1=top)
function concave_radius(t) =
    let(
        r_top = body_od_top / 2,
        r_bot = body_od_bottom / 2,
        r_waist = body_od_waist / 2,
        // Use a cosine curve for smooth concavity
        // Map t to a curve that dips at waist_pos
        phase = (t - body_waist_pos) / max(body_waist_pos, 1 - body_waist_pos),
        // Blend between edge radius and waist radius
        edge_r = r_bot + (r_top - r_bot) * t,
        dip = (1 - cos(phase * 180)) / 2,
        depth = edge_r - r_waist
    )
    edge_r - depth * (1 - abs(phase) < 1 ?
        (1 - pow(abs(t - body_waist_pos) / max(body_waist_pos, 1-body_waist_pos), 2)) :
        0);

// More precise concave profile using sine
function body_radius(t) =
    let(
        r_avg = (body_od_top/2 + body_od_bottom/2) / 2,
        r_waist = body_od_waist / 2,
        depth = r_avg - r_waist,
        // Sine curve peaks concavity at waist position
        s = sin(t / body_waist_pos * 90),
        s2 = sin((1-t) / (1-body_waist_pos) * 90),
        blend = t <= body_waist_pos ? s : s2,
        r_edge = t <= body_waist_pos ?
            body_od_bottom/2 + (r_waist - body_od_bottom/2 + depth) * (1 - blend) :
            body_od_top/2 + (r_waist - body_od_top/2 + depth) * (1 - blend)
    )
    // Simple approach: cosine blend
    let(
        r_top = body_od_top / 2,
        r_bot = body_od_bottom / 2,
        linear_r = r_bot + (r_top - r_bot) * t,
        concave_factor = sin(t * 180) // peaks at t=0.5
    )
    linear_r - (linear_r - body_od_waist/2) * pow(sin(t * 180), 1.5) *
        (body_waist_pos > 0 ? 1 : 0);

// Simplified concave radius function
function shell_r(t) =
    let(
        r_top = body_od_top / 2,
        r_bot = body_od_bottom / 2,
        r_waist = body_od_waist / 2,
        // Linear interpolation of edge
        r_lin = r_bot + (r_top - r_bot) * t,
        // Concavity envelope: sin curve, zero at top and bottom, max at middle
        envelope = sin(t * 180),
        // Max concavity depth
        max_depth = (r_bot + r_top)/2 - r_waist
    )
    r_lin - max_depth * pow(envelope, 1.3);


// --- Base Bottom Plate ----------------------------------------
module base_plate() {
    difference() {
        union() {
            // Main circular plate
            cylinder(d=base_od, h=plate_thick);

            // Screw bosses (raised rings for screws)
            for (i = [0:assy_screw_count-1]) {
                angle = i * 360 / assy_screw_count + 45;
                translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), 0])
                    cylinder(d=6, h=plate_thick);
            }
        }

        // Steel insert pockets (recessed into bottom)
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

        // Center hole for wiring/joystick clearance
        translate([0, 0, -0.1])
            cylinder(d=joy_base_w + 4, h=plate_thick + 0.2);
    }
}

// --- Base Ring ------------------------------------------------
module base_ring() {
    difference() {
        union() {
            // Outer wall
            difference() {
                cylinder(d=base_od, h=base_height);
                translate([0, 0, base_floor])
                    cylinder(d=base_od - 2*base_wall, h=base_height);
            }

            // Floor (internal floor at bottom)
            cylinder(d=base_od, h=base_floor);

            // PCB standoffs
            for (i = [0:3]) {
                angle = i * 90;
                translate([pcb_mount_spread * cos(angle), pcb_mount_spread * sin(angle), base_floor])
                    cylinder(d=pcb_standoff_d, h=pcb_standoff_h);
            }

            // Joystick module mount pad (center)
            translate([0, 0, base_floor])
                cylinder(d=joy_base_w + 8, h=3);

            // Screw bosses at top rim (for potential top attachment)
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

        // Joystick module clearance hole
        translate([0, 0, -0.1])
            cylinder(d=joy_base_w + 2, h=base_floor + 4);

        // Joystick stick clearance (through floor and up)
        translate([0, 0, -0.1])
            cylinder(d=joy_stick_d + 10, h=base_height + 0.2);

        // USB-C port cutout (at angle 0 = back)
        translate([base_od/2 - base_wall - 1, 0, usbc_z])
            rotate([0, 90, 0])
                rounded_slot(usbc_width, usbc_height, base_wall + 2);

        // Side button cutouts (left at -90°, right at +90°)
        for (side = [-1, 1]) {
            angle = side * side_btn_angle;
            translate([
                (base_od/2 - base_wall/2) * cos(angle),
                (base_od/2 - base_wall/2) * sin(angle),
                side_btn_z
            ])
            rotate([0, 0, angle])
            rotate([0, 90, 0])
                rounded_slot(side_btn_width, side_btn_height, base_wall + 2);
        }

        // Power switch cutout
        rotate([0, 0, sw_angle])
            translate([base_od/2 - base_wall - 1, 0, sw_z])
                rotate([0, 90, 0])
                    rounded_slot(sw_width, sw_height, base_wall + 2);

        // Assembly screw holes (bottom, countersunk from below)
        for (i = [0:assy_screw_count-1]) {
            angle = i * 360 / assy_screw_count + 45;
            translate([assy_screw_r * cos(angle), assy_screw_r * sin(angle), -0.1])
                cylinder(d=assy_screw_d, h=base_height + 0.2);
        }

        // Battery compartment clearance (one side of the base interior)
        translate([20, 0, base_floor + 0.1])
            cube([30, 40, 12], center=true);
    }
}

// --- Body Shell (Concave Cylinder) ----------------------------
module body_shell() {
    n = body_resolution;

    difference() {
        // Outer concave surface
        body_concave_solid(0);

        // Inner cavity (offset inward by wall thickness)
        translate([0, 0, -0.1])
            body_concave_solid(body_wall);

        // Hollow out top for top cap insertion
        translate([0, 0, body_height - top_cap_lip - 0.1])
            cylinder(d=body_od_top - 2*body_wall + tol, h=top_cap_lip + 0.2);
    }

    // Internal mounting ring at bottom (for joystick coupler)
    difference() {
        translate([0, 0, 0])
            cylinder(d=coupler_flange + 4, h=3);
        translate([0, 0, -0.1])
            cylinder(d=coupler_od + tol, h=3.2);
    }
}

// Generates the concave solid shape
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

// --- Top Cap --------------------------------------------------
module top_cap() {
    difference() {
        union() {
            // Top dome/disc
            cylinder(d=body_od_top, h=top_cap_height - top_cap_lip);

            // Internal lip (fits inside body shell)
            translate([0, 0, -(top_cap_lip)])
                cylinder(d=body_od_top - 2*body_wall - tol, h=top_cap_lip);
        }

        // Hollow inside (save material)
        translate([0, 0, top_cap_wall])
            cylinder(d=body_od_top - 2*top_cap_wall, h=top_cap_height);

        // Left button cutout
        translate([
            -(top_btn_spacing/2 + top_btn_width/2),
            top_btn_offset_y,
            -0.1
        ])
            rounded_rect(top_btn_width, top_btn_length, top_cap_height + 0.2, 2);

        // Right button cutout
        translate([
            (top_btn_spacing/2 + top_btn_width/2),
            top_btn_offset_y,
            -0.1
        ])
            rounded_rect(top_btn_width, top_btn_length, top_cap_height + 0.2, 2);

        // Internal lip hollow
        translate([0, 0, -(top_cap_lip) - 0.1])
            cylinder(d=body_od_top - 2*top_cap_wall - 2*body_wall, h=top_cap_lip + 0.2);
    }

    // Button switch mounts (posts for tactile switches)
    for (side = [-1, 1]) {
        translate([
            side * (top_btn_spacing/2 + top_btn_width/2),
            top_btn_offset_y - top_btn_length/2 - 3,
            -(top_cap_lip)
        ])
            cylinder(d=4, h=top_cap_lip + top_cap_wall - 1);
    }
}

// --- Top Button Cap -------------------------------------------
module button_cap_top() {
    cap_w = top_btn_width - 2*btn_cap_clearance;
    cap_l = top_btn_length - 2*btn_cap_clearance;

    difference() {
        union() {
            // Button surface (slightly domed)
            translate([0, 0, 0])
                rounded_rect(cap_w, cap_l, btn_cap_thickness, 1.5);

            // Hinge tab (one side, connects to cap frame)
            translate([0, -cap_l/2 - btn_cap_hinge_w/2, 0])
                cube([cap_w * 0.4, btn_cap_hinge_w, btn_cap_thickness * 0.5], center=true);
        }

        // Slight dome on top surface
        translate([0, 0, btn_cap_thickness + 15])
            scale([1, 1, 0.05])
                sphere(d=cap_w + 10);
    }

    // Switch plunger contact (underneath)
    translate([0, 0, -2])
        cylinder(d=3, h=2);
}

// --- Side Button Cap ------------------------------------------
module button_cap_side() {
    cap_w = side_btn_width - 2*btn_cap_clearance;
    cap_h = side_btn_height - 2*btn_cap_clearance;

    difference() {
        // Curved outer surface to match base cylinder
        intersection() {
            cube([side_btn_cap_thick + 2, cap_w, cap_h], center=true);
            translate([base_od/2 - base_wall, 0, 0])
                rotate([0, 0, 0])
                    difference() {
                        cylinder(d=base_od + 1, h=cap_h, center=true);
                        cylinder(d=base_od - 2, h=cap_h + 1, center=true);
                    }
        }
    }

    // Switch contact nub (inward)
    translate([-side_btn_cap_thick/2 - 1.5, 0, 0])
        cylinder(d=3, h=2, center=true);
}

// --- Joystick Coupler -----------------------------------------
module joystick_coupler() {
    difference() {
        union() {
            // Main cylinder
            cylinder(d=coupler_od, h=coupler_height);

            // Top flange (connects to body shell interior)
            translate([0, 0, coupler_height - coupler_flange_h])
                cylinder(d=coupler_flange, h=coupler_flange_h);
        }

        // Joystick stick bore (through hole)
        translate([0, 0, -0.1])
            cylinder(d=coupler_id, h=coupler_height + 0.2);

        // Set screw hole (to lock onto joystick stick)
        translate([0, 0, coupler_height * 0.4])
            rotate([90, 0, 0])
                cylinder(d=2, h=coupler_od, center=true);

        // Weight reduction (hollow upper section)
        translate([0, 0, coupler_height * 0.5])
            difference() {
                cylinder(d=coupler_od - 4, h=coupler_height * 0.5 - coupler_flange_h);
                cylinder(d=coupler_id + 4, h=coupler_height);
            }
    }
}

// --- Joystick Module (Reference/Ghost) ------------------------
module joystick_module_ref() {
    color("dimgray", 0.5) {
        // Base
        translate([-joy_base_w/2, -joy_base_d/2, 0])
            cube([joy_base_w, joy_base_d, joy_base_h]);
        // Stick
        cylinder(d=joy_stick_d, h=joy_base_h + joy_stick_h);
        // Stick knob
        translate([0, 0, joy_base_h + joy_stick_h])
            sphere(d=joy_stick_d + 2);
    }
}

// ============================================================
//                    UTILITY MODULES
// ============================================================

// Rounded rectangle (centered on XY, Z from 0)
module rounded_rect(w, l, h, r) {
    translate([0, 0, h/2])
        hull() {
            for (x = [-1, 1], y = [-1, 1])
                translate([x*(w/2-r), y*(l/2-r), 0])
                    cylinder(r=r, h=h, center=true);
        }
}

// Rounded slot (like USB-C port shape) — centered, along Z
module rounded_slot(w, h, depth) {
    r = h / 2;
    hull() {
        translate([0, -(w/2 - r), 0]) cylinder(r=r, h=depth);
        translate([0,  (w/2 - r), 0]) cylinder(r=r, h=depth);
    }
}

// ============================================================
//                      ASSEMBLY
// ============================================================

module assembly() {
    e = EXPLODE;

    // Base plate (bottom)
    color("SlateGray")
        translate([0, 0, -e])
            base_plate();

    // Base ring
    color("SteelBlue")
        translate([0, 0, plate_thick])
            base_ring();

    // Joystick module (ghost reference)
    translate([0, 0, plate_thick + base_floor])
        joystick_module_ref();

    // Joystick coupler
    color("Orange")
        translate([0, 0, plate_thick + base_floor + joy_base_h + joy_stick_h - coupler_height + e*0.5])
            joystick_coupler();

    // Body shell
    color("DodgerBlue", 0.85)
        translate([0, 0, plate_thick + base_height + tilt_clearance + e])
            body_shell();

    // Top cap
    color("CornflowerBlue")
        translate([0, 0, plate_thick + base_height + tilt_clearance + body_height + e*2])
            top_cap();

    // Top button caps (ghost)
    color("White", 0.9)
    for (side = [-1, 1]) {
        translate([
            side * (top_btn_spacing/2 + top_btn_width/2),
            top_btn_offset_y,
            plate_thick + base_height + tilt_clearance + body_height + top_cap_wall + e*2.5
        ])
            button_cap_top();
    }
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
else if (RENDER_PART == "top_cap") {
    top_cap();
}
else if (RENDER_PART == "button_top_left" || RENDER_PART == "button_top_right") {
    button_cap_top();
}
else if (RENDER_PART == "button_side") {
    button_cap_side();
}
else if (RENDER_PART == "joystick_coupler") {
    joystick_coupler();
}
else {
    echo("Unknown RENDER_PART. Use: assembly, base_plate, base_ring, body, top_cap, button_top_left, button_top_right, button_side, joystick_coupler");
}
