def answer_user_question(question, analysis_package, retrieved_contexts):
    q = question.lower()

    features = analysis_package["features"]
    fit_1rc = analysis_package["fit_1rc"]
    fit_2rc = analysis_package["fit_2rc"]

    min_v = features["Min Voltage (V)"]
    max_v = features["Max Voltage (V)"]
    max_abs_power = features["Max |Power| (W)"]

    context_text = "\n".join(retrieved_contexts) if retrieved_contexts else "No requirement context provided."

    if "voltage requirement" in q or ("voltage" in q and "requirement" in q):
        return (
            f"Retrieved requirement context:\n{context_text}\n\n"
            f"Measured battery result:\n"
            f"- Minimum voltage = {min_v} V\n"
            f"- Maximum voltage = {max_v} V\n\n"
            f"Initial assessment:\n"
            f"The test should be compared against the retrieved voltage-related requirement text above. "
            f"If the requirement specifies a minimum allowed voltage, compare it directly with {min_v} V. "
            f"This minimal agent surfaces the relevant requirement and measured result for first-pass engineering review."
        )

    if "power" in q:
        return (
            f"Retrieved requirement context:\n{context_text}\n\n"
            f"Measured battery result:\n"
            f"- Maximum absolute terminal power = {max_abs_power} W\n\n"
            f"Initial assessment:\n"
            f"This provides a first-pass answer for power-related behavior. "
            f"You can compare {max_abs_power} W against any requirement limits in the retrieved context."
        )

    if "ecm" in q or "1rc" in q or "2rc" in q or "fit" in q:
        return (
            f"Retrieved requirement context:\n{context_text}\n\n"
            f"ECM fitting summary:\n"
            f"- 1RC RMSE = {fit_1rc['rmse_v']:.6f} V\n"
            f"- 2RC RMSE = {fit_2rc['rmse_v']:.6f} V\n\n"
            f"Interpretation:\n"
            f"The lower-RMSE model provides a better first-pass fit for this dataset under the constant-OCV assumption."
        )

    return (
        f"Retrieved requirement context:\n{context_text}\n\n"
        f"Battery analysis summary:\n"
        f"- Min voltage = {min_v} V\n"
        f"- Max voltage = {max_v} V\n"
        f"- Max |power| = {max_abs_power} W\n"
        f"- 1RC RMSE = {fit_1rc['rmse_v']:.6f} V\n"
        f"- 2RC RMSE = {fit_2rc['rmse_v']:.6f} V\n\n"
        f"This minimal copilot combines retrieved engineering context with structured battery metrics to answer first-pass qualification questions."
    )