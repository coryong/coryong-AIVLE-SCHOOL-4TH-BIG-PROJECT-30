import pandas as pd

# 각각의 CSV 파일을 읽어옵니다.
df1 = pd.read_csv("results_blog_title_main_url_1.csv", encoding='utf-8-sig')
df2 = pd.read_csv("naver_title_main_img_url_url_1.csv", encoding='utf-8-sig')
df3 = pd.read_csv("youtube_videos_1.csv", encoding='utf-8')


# 세 DataFrame을 합칩니다.
merged_df = pd.concat([df1, df2, df3], ignore_index=True)
merged_df = merged_df.drop(columns=['Unnamed: 0'])

merged_df = merged_df[['title', 'body', 'image', 'url']]

# 합친 DataFrame에서 무작위로 30개를 선택합니다.
sample_df = merged_df.sample(n=30)


# 선택된 데이터를 새로운 CSV 파일로 저장합니다.
sample_df.to_csv("merged_sample.csv", index=False, encoding='utf-8-sig')
