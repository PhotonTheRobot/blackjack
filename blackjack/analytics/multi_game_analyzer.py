from statistics import mean
from textwrap import dedent

import matplotlib.pyplot as plt


class MultiGameAnalyzer:
    """Class for running basic analytics on tracked metrics for a multiple games."""

    def __init__(self, gameAnalyticsArray, loggingController):
        # All games have the same initial bankroll. Grab it from the first game.
        self._gameAnalyticsArray = gameAnalyticsArray
        self._primaryProfit = 0
        self._sidebetProfit = 0
        self._loggingController = loggingController

    def _aggregateMetrics(self):
        # Gross metric counts
        self._primaryProfit = sum([game.PrimaryProfit for game in self._gameAnalyticsArray])
        self._sidebetProfit = sum([game.SidebetProfit for game in self._gameAnalyticsArray])
        
        
    def print_summary(self):
        self._aggregateMetrics()
        
        # Return the formatted summary string
        print(dedent(f"""\
            --- Bankroll ---
               Total Games: {len(self._gameAnalyticsArray)}
            Primary Profit: {self._loggingController.GetMoneyFormat(self._primaryProfit)}
            Sidebet Profit: {self._loggingController.GetMoneyFormat(self._sidebetProfit)}
            """)
        )

    def create_plots(self):
        """Create charts summarizing the tracked metric data."""
        # Create a figure to hold the plots (called "axes")
        fig, (ax1, ax2) = plt.subplots(2, 1)  # 2 rows 1 column of axes (i.e. stacked plots)

        # Axes 1: Final Bankroll Distribution (Histogram)
        ax1.hist(self.final_bankrolls)
        ax1.set_xlabel('Final Bankroll ($)')
        ax1.set_ylabel('Count')
        ax1.set_title('Final Bankrolls')

        # Axes 2: Hand Outcome Breakdown (pie chart)
        data = []
        labels = []
        for metric, label in [
            (self.wins, 'Wins'), (self.losses, 'Losses'), (self.pushes, 'Pushes'), (self.insurance_wins, 'Insurance Wins')
        ]:
            if metric > 0:
                data.append(metric)
                labels.append(label)

        wedges, _, _ = ax2.pie(data, autopct=lambda pct: slice_label(pct, data), textprops=dict(color="w")) 
        ax2.legend(wedges, labels, title="Outcomes")
        ax2.set_title('Hand Outcomes')
        ax2.axis('equal')

        # Avoid plot label overlap
        plt.tight_layout()
        plt.show()
