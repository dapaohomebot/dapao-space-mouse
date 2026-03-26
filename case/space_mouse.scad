// ============================================================
// DaPao Space Mouse — Master Assembly File (v2)
// ============================================================
// Open this file in OpenSCAD to view the full assembly.
// Individual part files are in case/parts/ — open those to
// export individual STLs for printing.
//
// Parts:
//   1. base_plate       — bottom plate, steel inserts, rubber feet
//   2. base_ring        — PCB mounts, USB-C, power switch
//   3. body_shell       — concave hourglass body, side button cutouts
//   4. top_frame        — ring + divider holding L/R buttons
//   5. button_top_left  — left half-circle rocker button
//   6. button_top_right — right half-circle rocker button
//   7. button_side      — side button caps (print 2)
//   8. joystick_coupler — connects joystick stick to body
// ============================================================

// --- Render Control -------------------------------------------
RENDER_PART  = "assembly";
// Options: "assembly", "base_plate", "base_ring", "body",
//          "top_frame", "button_top_left", "button_top_right",
//          "button_side", "joystick_coupler"

CROSS_SECTION = false;
EXPLODE = 0;  // mm separation between parts in assembly view

// --- Include all part files -----------------------------------
include <parts/params.scad>
include <parts/base_plate.scad>
include <parts/base_ring.scad>
include <parts/body_shell.scad>
include <parts/top_frame.scad>
include <parts/button_top_left.scad>   // defines top_button_left()
include <parts/button_top_right.scad>  // defines top_button_right()
include <parts/button_side.scad>       // defines side_button_cap()
include <parts/joystick_coupler.scad>


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
    body_z     = plate_thick + base_height + tilt_clearance;
    top_z      = body_z + body_height;
    side_btn_z = body_z + body_height * side_btn_z_frac;

    color("SlateGray")
        translate([0, 0, -e])
            base_plate();

    color("SteelBlue")
        translate([0, 0, plate_thick])
            base_ring();

    translate([0, 0, plate_thick + base_floor])
        joystick_module_ref();

    color("Orange")
        translate([0, 0, plate_thick + base_floor + joy_base_h + joy_stick_h - coupler_height + e*0.5])
            joystick_coupler();

    color("DodgerBlue", 0.85)
        translate([0, 0, body_z + e])
            body_shell();

    color("SteelBlue")
        translate([0, 0, top_z + e*2])
            top_frame();

    color("White", 0.92)
        translate([0, 0, top_z + top_frame_height + e*2.5])
            top_button_left();

    color("WhiteSmoke", 0.92)
        translate([0, 0, top_z + top_frame_height + e*2.5])
            top_button_right();

    color("LightGray", 0.9)
        translate([0, 0, side_btn_z + e])
            rotate([0, 0, 90])
                translate([shell_r(side_btn_z_frac) - body_wall/2, 0, 0])
                    side_button_cap();

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
else if (RENDER_PART == "base_plate")      { base_plate(); }
else if (RENDER_PART == "base_ring")       { base_ring(); }
else if (RENDER_PART == "body")            { body_shell(); }
else if (RENDER_PART == "top_frame")       { top_frame(); }
else if (RENDER_PART == "button_top_left") { top_button_left(); }
else if (RENDER_PART == "button_top_right"){ top_button_right(); }
else if (RENDER_PART == "button_side")     { side_button_cap(); }
else if (RENDER_PART == "joystick_coupler"){ joystick_coupler(); }
else {
    echo("Unknown RENDER_PART. Options: assembly, base_plate, base_ring, body, top_frame, button_top_left, button_top_right, button_side, joystick_coupler");
}
