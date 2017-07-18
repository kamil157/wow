def get_talent_for_spec(spec, talent):
    try:
        spec_talent = next(t for t in talent if 'spec' in t and t['spec']['name'] == spec)
    except StopIteration:
        # If there is no spec info, this talent is for all specs which don't have a talent specified.
        spec_talent = next(t for t in talent if 'spec' not in t)
    return spec_talent['spell']