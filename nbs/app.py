import pandas as pd
import hvplot.pandas
import panel as pn
pn.extension('tabulator')


df = pd.read_csv("https://raw.githubusercontent.com/danhphan/credit-risk/main/data/interest_rates.csv")
df["date"] = pd.to_datetime(df["date"])

# Make DataFrame Pipeline Interactive
idf = df.interactive()

country_mapping = {"US":0, "UK":1, "AU":2} 
pred_results = {}

for idx, country in enumerate(country_mapping.keys()):
    # Prediction
    print(idx, country)
    df_data = pd.read_csv(f"https://raw.githubusercontent.com/danhphan/credit-risk/main/data/prediction_{country}.csv")
    df_data['Date'] = pd.to_datetime(df_data['Date'])
    df_data = df_data.set_index("Date")
    pred_results[country] = df_data


WIDTH = 550
chart_data = (idf.hvplot(x = 'date', by='country', y='rate', kind='scatter', 
                         xlabel="Date", ylabel="Observed interest rate", width=WIDTH,
                         line_width=2, title="Historical interest rates by Country") *
              idf.hvplot(x = 'date', by='country', y='rate', line_width=1, color=["blue", "green", "red"])
              ).opts(legend_position='top', legend_offset=(150, 0))



# Make DataFrame Pipeline Interactive
def plot(pred_results, country, color='red'):
    y_iteractivate = pred_results[country].interactive()
    panel_plot = (y_iteractivate.hvplot(label="10% Quantile", alpha=0.5, x="Date", y="Q10", width=WIDTH,
                        xlabel='Date', ylabel="Predicted interest rate", title=f'Prediction for {country}') * 
                  y_iteractivate.hvplot(label="90% Quantile", x="Date", y="Q90", alpha=0.3) *
                  y_iteractivate.hvplot(label='mean', x="Date", y="Mean", color=color, line_width=3) )
    return panel_plot.opts(legend_position='top', legend_offset=(150,0))



pred_au = plot(pred_results, 'AU', 'blue')
pred_us = plot(pred_results, 'US', 'green')
pred_uk = plot(pred_results, 'UK', 'red')

#Layout using Template
template = pn.template.FastListTemplate(
    title='Interest rates prediction for US, AU and UK', 
    sidebar=[pn.pane.Markdown("# Interest rates prediction"), 
             pn.pane.Markdown("#### Interest rates prediction for US, AU and UK. This project is used for technology demonstration purpose, and should not be used for the investment decision-making."), 
#              pn.pane.PNG('climate_day.png', sizing_mode='scale_both'),
             ],
    main=[pn.Row(pn.Column(chart_data.panel()), 
                 pred_au.panel()), 
          pn.Row(pn.Column(pred_us.panel()), 
                 pn.Column(pred_uk.panel()))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
    sizing_mode="stretch_both"
)

template.servable()
