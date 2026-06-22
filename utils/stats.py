import pandas as pd

def rolling_average(df, n):
    return df["seconds"].rolling(n).mean()

def personal_best(df):
    return df["seconds"].min()

def best_ao(df, n):
    # True Ao5/Ao12: drop best and worst, average the rest
    def trim_mean(window):
        s = sorted(window)
        return sum(s[1:-1]) / (n - 2)
    return df["seconds"].rolling(n).apply(trim_mean, raw=True).min()

def format_time(seconds: float) -> str:
    if seconds >= 60:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}:{s:05.2f}"
    return f"{seconds:.2f}"

def format_hour(hour: int) -> str:
    return f"{int(hour):02d}:00"

def time_of_day_performance(df, min_solves=5):
    hourly = (
        df.assign(hour=df["date"].dt.hour)
        .groupby("hour", as_index=False)
        .agg(
            average_solve=("seconds", "mean"),
            median_solve=("seconds", "median"),
            best_solve=("seconds", "min"),
            consistency=("seconds", "std"),
            solve_count=("seconds", "size"),
        )
    )

    hourly = pd.DataFrame({"hour": range(24)}).merge(hourly, on="hour", how="left")
    hourly["solve_count"] = hourly["solve_count"].fillna(0).astype(int)

    qualifying = hourly[hourly["solve_count"] >= min_solves].dropna(subset=["average_solve"])
    best_row = None

    if not qualifying.empty:
        best_row = qualifying.loc[qualifying["average_solve"].idxmin()]

    return hourly, best_row