def calculator_ration(data: dict) -> dict:
    current_asset = data.get("current_asset",0.0)
    current_liabilities = data.get("current_liabilities",0.0)
    total_debt = data.get("total_dept",0.0)
    total_equity = data.get("total_equity",0.0)
    ebit = data.get("ebit",0.0)
    interest_expense = data.get("interest_expense",0.0)
    retained_earning = data.get("retained_earning", 0.0)
    total_assets = data.get("total_assets",0.0)
    total_revenue = data.get("total_revenue",0.0)

    if current_liabilities > 0:
        current_ratio = round(current_asset/current_liabilities,2)
    else:
        current_ratio = None
    if total_equity > 0:
        debt_to_equity = round(total_debt/total_equity, 2)
    else:
        debt_to_equity = None
    if interest_expense > 0:
        interest_coverage = round(ebit/interest_expense,2)
    else:
        interest_coverage = None

    total_assets = float(
        data.get("total_assets")
        or data.get("total_asset")
        or data.get("assets")
        or 0.0
    )
    
    if total_assets <= 0 and (total_debt + total_equity) > 0:
        total_assets = total_debt + total_equity

    retained_earnings = float(data.get("retained_earnings", data.get("retained_earning", 0.0)) or 0.0)
    total_revenue = float(data.get("total_revenue", data.get("revenue", data.get("sales", 0.0))) or 0.0)

    # 2. Altman Z-Score Calculation
    if total_assets > 0 and total_debt > 0:
        altman_z_score = round(
            1.2 * ((current_asset - current_liabilities) / total_assets)
            + 1.4 * (retained_earnings / total_assets)
            + 3.3 * (ebit / total_assets)
            + 0.6 * (total_equity / total_debt)
            + 0.999 * (total_revenue / total_assets),
            2
        )
    else:
        altman_z_score = None
    #Risk flag
    flags = []
    if current_ratio is not None and current_ratio < 1.5:
        flags.append("WARNING: Low Liquidity (Current Ration below 1.5)")
    if  debt_to_equity is not None and debt_to_equity > 2.0:
        flags.append("WARNING: High Leverage (Debt to Equity below 2.0)")
    if  altman_z_score is not None and altman_z_score < 1.8:
        flags.append("CRITICAL: Company is in Distress Zone")
    return{
        "current_ratio": current_ratio,
        "debt_to_equity":debt_to_equity,
        "interest_coverage": interest_coverage,
        "altman_z_score" : altman_z_score,
        "flags": flags
    }

        