import uuid

generated_ids = set()

def generate_unique_id():
    new_id = uuid.uuid4().hex[:8]
    while new_id in generated_ids:
        new_id = uuid.uuid4().hex[:8]
    generated_ids.add(new_id)
    return new_id

print(generate_unique_id())