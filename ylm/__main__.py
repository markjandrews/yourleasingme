import difflib
from math import floor

import requests

from ylm import api
from ylm.config import config


def main(argv=None):
    api.web_request('POST', 'make', None)

    filter = set()
    for item in config['filter']:
        filter_item = [x.strip() for x in item.split(',')]
        filter_item.extend([''] * max(0, 5 - len(filter_item)))
        filter.add(tuple(filter_item))

    makes = api.get_makes()

    for make in makes.values():
        model_filter = set([x for x in filter if not x[0] or x[0] == '*' or x[0].lower() == make.name.lower()])

        if not model_filter:
            continue

        models = api.get_models(make)
        for model in models.values():
            years_filter = set(
                [x for x in model_filter if not x[1] or x[1] == '*' or x[1].lower() == model.name.lower()])

            if not years_filter:
                continue

            years = api.get_years(model)
            for year in years:
                bodies_filter = set([x for x in years_filter if not x[2] or x[2] == '*' or str(x[2]) == str(year)])

                if not bodies_filter:
                    continue

                # print(f'{model.name}, {make.name}, {year}')

                bodies = api.get_bodies(model, year)
                for body in bodies.values():
                    variants_filter = set(
                        [x for x in bodies_filter if not x[3] or x[3] == '*' or x[3].lower() == body.body_type.lower()])

                    if not variants_filter:
                        continue

                    # print(f'{model.name}, {make.name}, {year}, {body.body_type}')

                    variants = api.get_variants(body, year, model)
                    for variant in variants.values():
                        if not set([x for x in variants_filter if
                                    not x[4] or x[4] == '*' or x[4].lower() in variant.description.lower()]):
                            continue

                        print(f'{model.name}, {make.name}, {year}, {body.body_type}, {variant.description}')
                        variant = api.get_variantprice(variant)
                        quote = api.get_quote(kms="20000", salary="140000", state="act", term=36, variant=variant)

                        # Payments
                        fortnight_finance_payment = quote.finance_per_pay_cycle
                        annual_finance_payment = float(quote.finance_per_year)
                        month_finance_payment = float(annual_finance_payment) / 12

                        fortnight_total_budget = quote.total_budgets_per_pay_cycle_with_vmp
                        annual_total_budget = float(quote.total_budgets_per_year_with_vmp)
                        month_total_budget = float(annual_total_budget) / 12

                        fortnight_running_cost = float(fortnight_total_budget) - float(fortnight_finance_payment)
                        annual_running_cost = annual_total_budget - annual_finance_payment
                        month_running_cost = annual_running_cost / 12

                        fortnight_emp_cont = quote.ecm_gross_per_pay_cycle
                        annual_emp_cont = quote.ecm_gross_per_year
                        month_emp_cont = float(annual_emp_cont) / 12

                        fortnight_pre_tax = quote.pre_tax_per_pay_cycle_with_vmp
                        annual_pre_tax = quote.pre_tax_per_year_with_vmp
                        month_pre_tax = float(annual_pre_tax) / 12

                        fortnight_post_tax = quote.post_tax_per_pay_cycle
                        annual_post_tax = quote.ecm_gross_per_year
                        month_post_tax = float(annual_post_tax) / 12

                        annual_take_home_pay = quote.take_home_pay_per_year
                        annual_saving = float(annual_pre_tax) + float(annual_post_tax) - float(annual_take_home_pay)
                        month_saving = annual_saving / 12
                        fortnight_savign = annual_saving / 26

                        if hasattr(quote, 'take_home_pay_per_cycle'):
                            fortnight_total_cost_to_pay = quote.take_home_pay_per_cycle
                        else:
                            fortnight_total_cost_to_pay = -1

                        annual_total_cost_to_pay = quote.take_home_pay_per_year
                        month_total_costi_to_pay = float(annual_total_cost_to_pay) / 12

                        # Running Costs
                        fornight_reg = quote.reg_per_pay_cycle
                        annual_reg = quote.reg_per_year
                        month_reg = float(annual_reg) / 12

                        fortnight_insurance = quote.ins_per_pay_cycle
                        annual_insurance = quote.ins_per_year
                        month_insurance = float(annual_insurance) / 12

                        fortnight_fuel = quote.f_per_pay_cycle
                        annual_fuel = quote.f_per_year
                        month_fuel = float(annual_fuel) / 12

                        fortnight_fuel = quote.mfee_per_pay_cycle
                        annual_fuel = quote.mfee_per_year
                        month_fuel = float(annual_fuel) / 12

                        residual_payment = quote.vehicle_residual_gross

                        fuel_metro = variant.fuel_metro
                        fuel_country = variant.fuel_country
                        fuel_combined = variant.fuel_combined
                        warranty = (variant.warranty_years, variant.warranty_kms)
                        list_price = variant.list_price_gross


if __name__ == '__main__':
    main()
