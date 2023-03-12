def slice_data(data, start, end, category):
    sub_df = data.iloc[start:end]
    #select only the prompt and category columns
    prompts = sub_df[['prompt', category]]
    #change the name of the category column to expected
    prompts.rename(columns={category: 'expected'}, inplace=True)
    #convert to a dictionary where each key is test1, test2 and each value is a row from the dataframe
    prompts_dict = prompts.to_dict('index')
    return prompts_dict