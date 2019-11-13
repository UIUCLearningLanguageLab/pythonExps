import pandas as pd

num_to_run = 290


def give_subjs(csv):

    output_df = csv[csv['n_to_run']!=0]
    for index, row in output_df.iterrows():
        for num in range(row['n_to_run'] - 1):
            if row['n_to_run'] > 1:
                output_df = output_df.append(row)
            else:
                pass
    output_df = output_df.sample(n=num_to_run).reset_index().drop('index', axis=1).drop('n_to_run', axis=1).drop('n', axis=1)
    output_df.rename(columns={'biggest_subj_num': 'subj_num'}, inplace=True)
    tracker_dict = {}
    for index, row in output_df.iterrows():
        cond = str(row['task']) + '_' + str(row['soa']) + '_' + str(row['rp']) + '_' + str(row['list'])
        tracker(row, cond, tracker_dict)
        output_df.at[index, 'subj_num'] = tracker_dict[str(cond)]
    return output_df


def tracker(row, cond, tracker_dict):
    try:
        tracker_dict[str(cond)] += 1
    except KeyError:
        tracker_dict[str(cond)] = row['subj_num'] + 1
    return tracker_dict


def main():
    csv_df = pd.read_csv('Superprime_Subject_Counts.csv')
    to_run = give_subjs(csv_df)
    to_run.to_csv('to_run.csv')


main()
