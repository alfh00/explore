import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class CandlePlot:

    def __init__(self, df):
        self.df_plot = df.copy()
        self.create_candle_fig()

    def create_candle_fig(self):
        # Create subplots: 1 row for candles, 1 row for TRIX
        self.fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,  # Adjust spacing between subplots
            row_heights=[1.2, 0.3]  # Adjust subplot heights
        )
        # Add candlestick trace to the first row
        self.fig.add_trace(
            go.Candlestick(
                x=self.df_plot.index,
                open=self.df_plot.open,
                high=self.df_plot.high,
                low=self.df_plot.low,
                close=self.df_plot.close,
                line=dict(width=1), opacity=1,
                increasing_fillcolor='#24A06B',
                decreasing_fillcolor='#CC2E3C',
                increasing_line_color='#2EC886',
                decreasing_line_color='#FF3A4C',
                name='Candles'
            ),
            row=1, col=1
        )

    def update_layout(self, width, height, nticks):
        self.fig.update_yaxes(
            gridcolor='#1F292F'
        )
        self.fig.update_xaxes(
            gridcolor='#1F292F',
            rangeslider=dict(visible=False),
            nticks=nticks
        )
        self.fig.update_layout(
            width=width,
            height=height,
            paper_bgcolor='#2C303C',
            plot_bgcolor='#2C303C',
            font=dict(size=12, color='#E1E1E1')
        )
        self.fig.update_layout(
            xaxis=dict(
            rangeslider=dict(
            visible=False
            ),
            type="date"
            )
        )

    def add_traces(self, line_traces):
        for t in line_traces:
            if t.startswith('TRIX'):
                # Add TRIX trace to the second row
                self.fig.add_trace(
                    go.Scatter(
                        x=self.df_plot.index,
                        y=self.df_plot[t],
                        line=dict(width=2),
                        name=t
                    ),
                    row=2, col=1
                )
            else:
                # Add other traces to the first row
                self.fig.add_trace(
                    go.Scatter(
                        x=self.df_plot.index,
                        y=self.df_plot[t],
                        line=dict(width=2),
                        line_shape='spline',
                        name=t
                    ),
                    row=1, col=1
                )

    def add_entries(self, trades):
        df = trades.copy()
        long_entries = df[df['position'] == 'LONG']
        self.fig.add_trace(go.Scatter(
            x=long_entries['open_date'], 
            y=long_entries['open_price'],
            mode='markers',
            marker=dict(color='green', size=5),
            name='Long Entry'
        ))

        # Add exit points for LONG trades (in light green)
        self.fig.add_trace(go.Scatter(
            x=long_entries['close_date'], 
            y=long_entries['close_price'],
            mode='markers',
            marker=dict(color='lightgreen', size=5),
            name='Long Exit'
        ))

        # Add entry points for SHORT trades (in red)
        short_entries = df[df['position'] == 'SHORT']
        self.fig.add_trace(go.Scatter(
            x=short_entries['open_date'], 
            y=short_entries['open_price'],
            mode='markers',
            marker=dict(color='red', size=5),
            name='Short Entry'
        ))

        # Add exit points for SHORT trades (in light red)
        self.fig.add_trace(go.Scatter(
            x=short_entries['close_date'], 
            y=short_entries['close_price'],
            mode='markers',
            marker=dict(color='lightcoral', size=5),
            name='Short Exit'
        ))

    def add_points(self, signals):
        
        long_entries = self.df_plot[self.df_plot[f'{signals}'] == 1]
        self.fig.add_trace(go.Scatter(
            x=long_entries.index, 
            y=long_entries.high,
            mode='markers',
            marker=dict(color='green', size=5),
            name='Long Entry'
        ))

        # Add entry points for SHORT trades (in red)
        short_entries = self.df_plot[self.df_plot[f'{signals}'] == -1]
        self.fig.add_trace(go.Scatter(
            x=short_entries.index, 
            y=short_entries.low,
            mode='markers',
            marker=dict(color='red', size=5),
            name='Short Entry'
        ))


    def show_plot(self, width=1200, height=600, nticks=5, line_traces=[]):
        self.add_traces(line_traces)
        self.update_layout(width, height, nticks)
        self.fig.show()