plt.figure(figsize=(20,0))
plt.title("Attack Frequency by Motive")
sb.countplot(data=df, y='Motive', color=sb.color_palette()[2],
             order=motive_order)
plt.xticks(rotation=45);
plt.figure(figsize=(20,0))
plt.title("Attack Frequency by Industry")
sb.countplot(data=df, y='Industry', color=sb.color_palette()[2],
             order=industry_order)
plt.xticks(rotation=45);
