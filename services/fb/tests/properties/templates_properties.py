def add_property_template(
    name="",
    prop_name="",
    primitive_type="STR",
    help_text="",
    is_required=False,
    is_multiple=False,
    validation="",
):
    return {
        "name": name,
        "properties": [
            {
                "name": prop_name,
                "primitive_type": primitive_type,
                "help_text": help_text,
                "is_required": is_required,
                "is_multiple": is_multiple,
                "validation": validation,
            }
        ],
    }


def get_properties_template(name="", is_deleted=False):
    return {"name": name, "is_deleted": is_deleted}
