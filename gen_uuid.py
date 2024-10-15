import uuid
def generate_unique_id():
    new_id = str(uuid.uuid4())
    while new_id in generated_ids:
        new_id = str(uuid.uuid4())
    generated_ids.add(new_id)
    return new_id
