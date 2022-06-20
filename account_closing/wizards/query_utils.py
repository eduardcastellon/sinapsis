# -*- coding: utf-8 -*-

PYG_QUERY = """
    with apuntes as (
        select
            account_id,
            (select code from account_account where id = l.account_id),
            --partner_id,
            --tax_line_id,
            sum(debit) as debit,
            sum(credit) as credit,
            sum(debit)-sum(credit) as new_balance,
            case when sum(debit)-sum(credit) > 0 then
                sum(debit)-sum(credit) else 0.00 end as new_debit,
            case when sum(debit)-sum(credit) < 0 then
                sum(credit)-sum(debit) else 0.00 end as new_credit,
            -- (SELECT user_type_id FROM account_account
                -- WHERE id=l.account_id) as user_type_id,
            tax_exigible,
            currency_id
        from
            account_move_line l
        where
            date <= date '{end_date}' and
            date >= date '{start_date}' and
            move_id in
                (select id from account_move
                    where state = 'posted' and company_id = {company_id})
        group by
            account_id, --partner_id, --tax_line_id, user_type_id,
            tax_exigible,
            currency_id
        having
            abs(sum(debit)-sum(credit))>0.001)

    insert into account_move_line(
        move_id,
        debit,
        credit,
        balance,
        -- debit_cash_basis, -- not exist
        -- credit_cash_basis, -- not exist
        -- balance_cash_basis, -- not exist
        company_currency_id,
        account_id,
        ref,
        reconciled,
        blocked,
        date,
        date_maturity,
        company_id,
        -- user_type_id,  -- not exist
        tax_exigible,
        create_uid,
        create_date,
        write_uid,
        write_date,
        currency_id -- not-null contraint
    )
    select
        {move_id},
        new_credit,
        new_debit,
        -new_balance,
        -- new_credit, new_debit, -new_balance,
        1,
        account_id,
        '{reference}',
        false,
        false,
        date '{date}',
        date '{date}',
        1,
        -- user_type_id,
        tax_exigible,
        1,
        now(),
        1,
        now(),
        currency_id -- not-null contraint
    from
        apuntes
    where
        account_id in
            (select id from account_account
                where code ilike '6%' or code ilike '7%')
    union
    select
        {move_id},

        case when sum(new_debit-new_credit) > 0 then
            sum(new_debit-new_credit) else 0.00 end as debit,
        
        case when sum(new_debit-new_credit) < 0 then
            abs(sum(new_debit-new_credit)) else 0.00 end as credit,

        sum(new_balance),
        -- sum(new_debit-new_credit), 0, sum(new_balance),
        1,
        {account_129},
        '{reference}',
        false,
        false,
        date '{date}',
        date '{date}',
        1,
        -- 11, -- user_type_id ?
        false,
        1,
        now(),
        1,
        now(),
        currency_id -- not-null contraint
    from
        apuntes
    where
        account_id in
            (select id from account_account
                where code ilike '6%' or code ilike '7%')
    group by
        currency_id"""

CLOSE_QUERY = """
    with apuntes as (
        select
            account_id,
            (select code from account_account where id = l.account_id),
            --partner_id,
            --tax_line_id,
            sum(debit) as debit,
            sum(credit) as credit,
            sum(debit)-sum(credit) as new_balance,
            case when sum(debit)-sum(credit) > 0 then
                sum(debit)-sum(credit) else 0.00 end as new_debit,
            case when sum(debit)-sum(credit) < 0 then
                sum(credit)-sum(debit) else 0.00 end as new_credit,
            -- user_type_id,
            tax_exigible,
            currency_id
        from
            account_move_line l
        where
            date <= date '{end_date}' and
            date >= date '{start_date}' and
            move_id in (select id from account_move
                where (state = 'posted' and company_id = {company_id})
                    {account_move_pyg_condition})
        group by
            account_id, --partner_id, --tax_line_id, user_type_id,
            tax_exigible,
            currency_id
        having
            abs(sum(debit)-sum(credit))>0.001)

    insert into account_move_line(
        move_id,
        debit,
        credit,
        balance,
        -- debit_cash_basis, credit_cash_basis, balance_cash_basis,
        company_currency_id,
        account_id,
        ref,
        reconciled,
        blocked,
        date,
        date_maturity,
        company_id,
        -- user_type_id,
        tax_exigible,
        create_uid,
        create_date,
        write_uid,
        write_date,
        currency_id -- not-null contraint
    )
    select
        {move_id},
        round(new_credit,2),
        round(new_debit,2),
        round(-new_balance,2),
        -- round(new_credit,2), round(new_debit,2), round(-new_balance,2),
        1,
        account_id,
        '{reference}',
        false,
        false,
        date '{date}',
        date '{date}',
        1,
        -- user_type_id,
        tax_exigible,
        1,
        now(),
        1,
        now(),
        currency_id -- not-null contraint
    from
        apuntes"""

OPEN_QUERY = """
    with apuntes as (
        select account_id,
        (select code from account_account where id = l.account_id),
        --partner_id, (select name from res_partner where id = l.partner_id),
        --tax_line_id,
        sum(debit) as debit,
        sum(credit) as credit,
        sum(debit)-sum(credit) as new_balance,
        case when sum(debit)-sum(credit) > 0 then
            sum(debit)-sum(credit) else 0.00 end as new_debit,
        case when sum(debit)-sum(credit) < 0 then
            sum(credit)-sum(debit) else 0.00 end as new_credit,
        -- user_type_id,
        tax_exigible,
        currency_id
    from
        account_move_line l
    where
        date <= date '{end_date}' and
        date >= date '{start_date}' and
        move_id in (select id from account_move
            where (state = 'posted' and company_id = {company_id})
                {account_move_pyg_condition})
    group by
        account_id, --partner_id, --tax_line_id, user_type_id,
        tax_exigible,
        currency_id
    having
        abs(sum(debit)-sum(credit))>0.001)

    insert into account_move_line(
        move_id,
        debit,
        credit,
        balance,
        --- debit_cash_basis, credit_cash_basis, balance_cash_basis,
        company_currency_id,
        account_id,
        ref,
        reconciled,
        blocked,
        date,
        date_maturity,
        company_id,
        -- user_type_id,
        tax_exigible,
        create_uid, create_date, write_uid, write_date,
        currency_id -- not-null contraint
    )
    select
        {move_id},
        round(new_debit,2),
        round(new_credit,2),
        round(new_balance,2),
        --round(new_debit,2), round(new_credit,2), round(new_balance,2),
        1,
        account_id,
        '{reference}',
        false,
        false,
        date '{date}',
        date '{date}',
        1,
        -- user_type_id,
        tax_exigible,
        1,
        now(),
        1,
        now(),
        currency_id -- not-null contraint
    from
        apuntes"""