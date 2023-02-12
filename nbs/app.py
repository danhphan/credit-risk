import numpy as np
import pandas as pd
import xarray as xr
import hvplot.pandas
import hvplot.xarray
import panel as pn
pn.extension('tabulator')

def build_XY(input_list,output_list=None,index=None):
    num_outputs = len(input_list)
    if output_list is not None:
        assert num_outputs == len(output_list)
        Y = np.vstack(output_list)
    else:
        Y = None

    if index is not None:
        assert len(index) == num_outputs
        I = np.hstack( [np.repeat(j,_x.shape[0]) for _x,j in zip(input_list,index)] )
    else:
        I = np.hstack( [np.repeat(j,_x.shape[0]) for _x,j in zip(input_list,range(num_outputs))] )

    X = np.vstack(input_list)
    X = np.hstack([X,I[:,None]])

    return X,Y,I[:,None] #slices


df = pd.read_csv("./data/interest_rates.csv")
df["date"] = pd.to_datetime(df["date"])

n_outputs = 3
country_mapping = {"US":0, "UK":1, "AU":2} 
M = 90
x_new = np.linspace(0, M-1, M)[:, None]
X_new, _, _ = build_XY([x_new for idx in range(n_outputs)])

dates_idx = pd.DataFrame({"date":pd.date_range("2016-01-01", "2023-06-01", freq='MS')}).reset_index()
dates_idx = dates_idx.rename(columns={"index":"x"})
print(dates_idx.shape)
dates_idx.head()


pred_results = {}

for idx, country in enumerate(country_mapping.keys()):
    # Prediction
    print(idx, country)
    pred_results[country] = xr.open_dataset(f"./nbs/{country}.nc")


# Make DataFrame Pipeline Interactive
idf = df.interactive()

WIDTH = 600


chart_data = (idf.hvplot(x = 'date', by='country', y='rate', kind='scatter', xlabel="Date", ylabel="Observed interest rate", 
                         line_width=2, title="Interest rates by Country", width=WIDTH) *
              idf.hvplot(x = 'date', by='country', y='rate', line_width=1)
              ).opts(legend_position='top', legend_offset=(150, 0))



def plot(pred_results, country):
    y_iteractivate = pred_results[country].interactive()
    panel_plot = (y_iteractivate.quantile(q=0.1, dim="draw").hvplot(label="10% Quantile", alpha=0.5, 
                        xlabel='Date', ylabel="Predicted interest rate", width=WIDTH, title=f'Prediction for {country}') * 
                  y_iteractivate.quantile(q=0.9, dim="draw").hvplot(label="90% Quantile", alpha=0.5) *
                  y_iteractivate.mean(dim="draw").hvplot(label='mean', color='red', line_width=3) )
    return panel_plot.opts(legend_position='top', legend_offset=(150,0))


pred_au = plot(pred_results, 'AU')
pred_us = plot(pred_results, 'US')
pred_uk = plot(pred_results, 'UK')


#Layout using Template
template = pn.template.FastListTemplate(
    title='Interest rates prediction for US, AU and UK', 
    sidebar=[pn.pane.Markdown("# Interest rates prediction"), 
             pn.pane.Markdown("#### Interest rates prediction for US, AU and UK. This project is used for technology demonstration purpose, and should not be used for the investment decision-making."), 
#              pn.pane.PNG('climate_day.png', sizing_mode='scale_both'),
             ],
    main=[pn.Row(pn.Column(chart_data.panel(width=WIDTH), margin=(0,25)), 
                 pred_au.panel(width=WIDTH)), 
          pn.Row(pn.Column(pred_us.panel(width=WIDTH), margin=(0,25)), 
                 pn.Column(pred_uk.panel(width=WIDTH)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
# template.show()
template.servable();















#Layout using Template
template = pn.template.FastListTemplate(
    title='Interest rates prediction for US, AU and UK', 
    sidebar=[pn.pane.Markdown("# Interest rates prediction"), 
             pn.pane.Markdown("#### Interest rates prediction for US, AU and UK. This project is used for technology demonstration purpose, and should not be used for the investment decision-making."), 
#              pn.pane.PNG('climate_day.png', sizing_mode='scale_both'),
             ],
    main=[pn.Row(pn.Column(chart_data.panel(width=WIDTH), margin=(0,25)), 
                 pred_au.panel(width=WIDTH)), 
          pn.Row(pn.Column(pred_us.panel(width=WIDTH), margin=(0,25)), 
                 pn.Column(pred_uk.panel(width=WIDTH)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
# template.show()
template.servable();