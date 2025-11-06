"""
Diagnostic script to find scale-related properties in Live's API
This will log all available properties to help us find the scale settings
"""

def log_all_properties(obj, name, log_func):
    """Log all properties and methods of an object"""
    log_func(f"\n{'='*60}")
    log_func(f"Properties of {name}:")
    log_func(f"{'='*60}")

    all_attrs = dir(obj)

    # Filter out private attributes
    public_attrs = [attr for attr in all_attrs if not attr.startswith('_')]

    for attr in sorted(public_attrs):
        try:
            value = getattr(obj, attr)
            value_type = type(value).__name__

            # Try to get a string representation
            try:
                if callable(value):
                    log_func(f"  {attr}() - method")
                else:
                    value_str = str(value)[:50]  # Limit length
                    log_func(f"  {attr} = {value_str} ({value_type})")
            except:
                log_func(f"  {attr} - {value_type}")
        except Exception as e:
            log_func(f"  {attr} - Error: {e}")

def find_scale_properties(c_instance):
    """Search for scale-related properties"""
    log_func = c_instance.log_message

    log_func("\n" + "="*60)
    log_func("DIAGNOSTIC MODE - Searching for Scale Properties")
    log_func("="*60)

    song = c_instance.song()

    # Check Song object
    log_func("\n### Checking Song object ###")
    scale_related = []
    for attr in dir(song):
        if 'scale' in attr.lower() or 'note' in attr.lower() or 'root' in attr.lower():
            try:
                value = getattr(song, attr)
                scale_related.append((attr, type(value).__name__))
                log_func(f"  FOUND: song.{attr} - {type(value).__name__}")
            except:
                pass

    # Check View object
    log_func("\n### Checking Song View object ###")
    view = song.view
    for attr in dir(view):
        if 'scale' in attr.lower() or 'note' in attr.lower() or 'root' in attr.lower():
            try:
                value = getattr(view, attr)
                scale_related.append((attr, type(value).__name__))
                log_func(f"  FOUND: song.view.{attr} - {type(value).__name__}")
            except:
                pass

    # Check selected track
    log_func("\n### Checking Selected Track ###")
    track = view.selected_track
    for attr in dir(track):
        if 'scale' in attr.lower() or 'note' in attr.lower():
            try:
                value = getattr(track, attr)
                scale_related.append((attr, type(value).__name__))
                log_func(f"  FOUND: track.{attr} - {type(value).__name__}")
            except:
                pass

    # Check if there's a clip
    if track.clip_slots and len(track.clip_slots) > 0:
        for slot in track.clip_slots:
            if slot.has_clip:
                clip = slot.clip
                log_func("\n### Checking Clip object ###")
                for attr in dir(clip):
                    if 'scale' in attr.lower() or 'note' in attr.lower():
                        try:
                            value = getattr(clip, attr)
                            scale_related.append((attr, type(value).__name__))
                            log_func(f"  FOUND: clip.{attr} - {type(value).__name__}")
                        except:
                            pass
                break

    log_func(f"\n### SUMMARY: Found {len(scale_related)} scale-related properties ###")
    for attr, attr_type in scale_related:
        log_func(f"  - {attr} ({attr_type})")

    log_func("\n" + "="*60)
    log_func("DIAGNOSTIC COMPLETE - Check Log.txt for results")
    log_func("="*60)
