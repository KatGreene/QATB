import bpy


class QATB_SoundBakeProperties(bpy.types.PropertyGroup):

    audio_file_path: bpy.props.StringProperty(
        name="Audio File Path",
        description="Path to the audio file",
        default="",
        subtype='FILE_PATH'
    ) # type: ignore

    low_frequency: bpy.props.FloatProperty(
        name="Low Frequency",
        description="Low frequency range for baking",
        default=20.0,
        min=20.0,
        max=20000.0,
        precision=1,
    ) # type: ignore
    
    high_frequency: bpy.props.FloatProperty(
        name="High Frequency",
        description="High frequency range for baking",
        default=200.0,
        min=20.0,
        max=20000.0,
        precision=1,
    ) # type: ignore

    attack_time: bpy.props.FloatProperty(
        name="Attack Time",
        description="Time in seconds for the sound to reach full volume",
        default=0.08,
        min=0.01,
        max=3.0,
    ) # type: ignore

    release_time: bpy.props.FloatProperty(
        name="Release Time",
        description="Time in seconds for the sound to decay to silence",
        default=0.5,
        min=0.01,
        max=3.0,
    ) # type: ignore

    threshold: bpy.props.FloatProperty(
        name="Threshold",
        description="Threshold volume for baking",
        default=0.0,
        min=0.0,
        max=1.0,
    ) # type: ignore

    freq_step: bpy.props.FloatProperty(
        name="Freq Step",
        description="Frequency step",
        default=500,
        min=0.1,
        max=20000,
        precision=1,
    ) # type: ignore

    log_mode: bpy.props.BoolProperty(
        name="Log Mode",
        description="Enable Log Mode for Frequency",
        default=False,
    ) # type: ignore

    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scale the Curve Value",
        default=1,
        min=0.01,
        max=2048,
        precision=2,
    ) # type: ignore

    fc_data_path : bpy.props.EnumProperty(
        items=[
            ("location", "Location", "Location"),
            ("rotation_euler", "Rotation", "Rotation"),
            ("scale", "Scale", "Scale")
        ],
        default="scale",
        description="Choose data path"
    ) # type: ignore

    fc_index : bpy.props.EnumProperty(
        items=[
            ("X", "X", "X"),
            ("Y", "Y", "Y"),
            ("Z", "Z", "Z")
        ],
        default="Z",
        description="Choose index"
    ) # type: ignore

    sound_bpm_value : bpy.props.IntProperty(
        name="Sound BPM Value",
        description="Sound BPM Value for beat generating",
        default=120,
        min=1,
        max=2048,
    ) # type: ignore


class QATB_AddArrayProperties(bpy.types.PropertyGroup):

    array_count: bpy.props.IntProperty(
        name="Array Count",
        description="The Count of the Array",
        default=10,
        min=1,
        max=100,
    ) # type: ignore

    relative_offset: bpy.props.FloatProperty(
        name="Relative Offset",
        description="The Relative Offset of the Array",
        default=1.5,
        min=0,
        max=2048.0,
        precision=2,
    ) # type: ignore
    