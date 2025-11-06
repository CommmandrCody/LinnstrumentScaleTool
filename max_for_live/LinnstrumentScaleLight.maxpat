{
	"patcher": {
		"fileversion": 1,
		"appversion": {
			"major": 8,
			"minor": 5,
			"revision": 0
		},
		"rect": [100.0, 100.0, 800.0, 600.0],
		"bglocked": 0,
		"openinpresentation": 1,
		"default_fontsize": 12.0,
		"default_fontface": 0,
		"default_fontname": "Arial",
		"gridonopen": 1,
		"gridsize": [15.0, 15.0],
		"gridsnaponopen": 1,
		"objectsnaponopen": 1,
		"statusbarvisible": 2,
		"toolbarvisible": 1,
		"lefttoolbarpinned": 0,
		"toptoolbarpinned": 0,
		"righttoolbarpinned": 0,
		"bottomtoolbarpinned": 0,
		"toolbars_unpinned_last_save": 0,
		"tallnewobj": 0,
		"boxanimatetime": 200,
		"enablehscroll": 1,
		"enablevscroll": 1,
		"boxes": [
			{
				"box": {
					"id": "obj-1",
					"maxclass": "comment",
					"text": "Linnstrument Scale Light",
					"fontsize": 18.0,
					"presentation": 1,
					"presentation_rect": [10.0, 10.0, 280.0, 25.0],
					"patching_rect": [10.0, 10.0, 280.0, 25.0],
					"numinlets": 1,
					"numoutlets": 0
				}
			},
			{
				"box": {
					"id": "obj-2",
					"maxclass": "live.menu",
					"varname": "root_note",
					"text": "Root Note",
					"parameter_enable": 1,
					"presentation": 1,
					"presentation_rect": [10.0, 45.0, 100.0, 20.0],
					"patching_rect": [10.0, 50.0, 100.0, 20.0],
					"saved_attribute_attributes": {
						"valueof": {
							"parameter_enum": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
							"parameter_initial": [0],
							"parameter_initial_enable": 1,
							"parameter_longname": "root_note",
							"parameter_mmax": 11,
							"parameter_shortname": "Root",
							"parameter_type": 2,
							"parameter_unitstyle": 9
						}
					},
					"numinlets": 1,
					"numoutlets": 3,
					"outlettype": ["", "", "int"]
				}
			},
			{
				"box": {
					"id": "obj-3",
					"maxclass": "live.menu",
					"varname": "scale_type",
					"text": "Scale",
					"parameter_enable": 1,
					"presentation": 1,
					"presentation_rect": [120.0, 45.0, 150.0, 20.0],
					"patching_rect": [120.0, 50.0, 150.0, 20.0],
					"saved_attribute_attributes": {
						"valueof": {
							"parameter_enum": ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian", "harmonic_minor", "melodic_minor", "major_pentatonic", "minor_pentatonic", "blues", "whole_tone", "chromatic", "diminished", "augmented", "bebop_major", "bebop_minor", "altered"],
							"parameter_initial": [0],
							"parameter_initial_enable": 1,
							"parameter_longname": "scale_type",
							"parameter_mmax": 19,
							"parameter_shortname": "Scale",
							"parameter_type": 2,
							"parameter_unitstyle": 9
						}
					},
					"numinlets": 1,
					"numoutlets": 3,
					"outlettype": ["", "", "int"]
				}
			},
			{
				"box": {
					"id": "obj-4",
					"maxclass": "live.toggle",
					"varname": "use_degrees",
					"text": "Degree Colors",
					"parameter_enable": 1,
					"presentation": 1,
					"presentation_rect": [10.0, 75.0, 60.0, 20.0],
					"patching_rect": [10.0, 85.0, 60.0, 20.0],
					"saved_attribute_attributes": {
						"valueof": {
							"parameter_initial": [0],
							"parameter_initial_enable": 1,
							"parameter_longname": "use_degrees",
							"parameter_shortname": "Degrees",
							"parameter_type": 2
						}
					},
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": ["int"]
				}
			},
			{
				"box": {
					"id": "obj-5",
					"maxclass": "comment",
					"text": "Use Degree Colors (I, III, V)",
					"fontsize": 11.0,
					"presentation": 1,
					"presentation_rect": [75.0, 77.0, 195.0, 18.0],
					"patching_rect": [75.0, 87.0, 195.0, 18.0],
					"numinlets": 1,
					"numoutlets": 0
				}
			},
			{
				"box": {
					"id": "obj-6",
					"maxclass": "live.button",
					"varname": "update_button",
					"text": "Update Lights",
					"parameter_enable": 1,
					"presentation": 1,
					"presentation_rect": [10.0, 105.0, 130.0, 30.0],
					"patching_rect": [10.0, 120.0, 130.0, 30.0],
					"saved_attribute_attributes": {
						"valueof": {
							"parameter_longname": "update_button",
							"parameter_shortname": "Update",
							"parameter_type": 2
						}
					},
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-7",
					"maxclass": "live.button",
					"varname": "clear_button",
					"text": "Clear Lights",
					"parameter_enable": 1,
					"presentation": 1,
					"presentation_rect": [150.0, 105.0, 120.0, 30.0],
					"patching_rect": [150.0, 120.0, 120.0, 30.0],
					"saved_attribute_attributes": {
						"valueof": {
							"parameter_longname": "clear_button",
							"parameter_shortname": "Clear",
							"parameter_type": 2
						}
					},
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-8",
					"maxclass": "newobj",
					"text": "shell",
					"patching_rect": [10.0, 200.0, 100.0, 22.0],
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-9",
					"maxclass": "newobj",
					"text": "sprintf set_scale %s %s false",
					"patching_rect": [10.0, 170.0, 200.0, 22.0],
					"numinlets": 2,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-10",
					"maxclass": "newobj",
					"text": "fromsymbol",
					"patching_rect": [10.0, 80.0, 100.0, 22.0],
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-11",
					"maxclass": "newobj",
					"text": "fromsymbol",
					"patching_rect": [120.0, 80.0, 100.0, 22.0],
					"numinlets": 1,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-12",
					"maxclass": "message",
					"text": "python3 linnstrument_scale_light.py $1",
					"patching_rect": [10.0, 230.0, 300.0, 22.0],
					"numinlets": 2,
					"numoutlets": 1,
					"outlettype": [""]
				}
			},
			{
				"box": {
					"id": "obj-13",
					"maxclass": "comment",
					"text": "Status:",
					"fontsize": 11.0,
					"presentation": 1,
					"presentation_rect": [10.0, 145.0, 260.0, 18.0],
					"patching_rect": [10.0, 270.0, 260.0, 18.0],
					"numinlets": 1,
					"numoutlets": 0
				}
			}
		],
		"lines": [
			{
				"patchline": {
					"source": ["obj-2", 1],
					"destination": ["obj-10", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-3", 1],
					"destination": ["obj-11", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-10", 0],
					"destination": ["obj-9", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-11", 0],
					"destination": ["obj-9", 1]
				}
			},
			{
				"patchline": {
					"source": ["obj-6", 0],
					"destination": ["obj-9", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-9", 0],
					"destination": ["obj-12", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-12", 0],
					"destination": ["obj-8", 0]
				}
			},
			{
				"patchline": {
					"source": ["obj-7", 0],
					"destination": ["obj-8", 0]
				}
			}
		]
	}
}
