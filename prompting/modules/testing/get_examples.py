import slice_data

def get_examples(data, start, end, category):
    prompts_dict = slice_data(data, start, end, category)
    examples = []
    for key, value in prompts_dict.items():
        examples.append({
            "input": value['prompt'],
            "output": value['expected']
        })
    return examples