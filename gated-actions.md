# gated actions: the things no agent does alone

> template. copy this file into your business folder and fill in the blanks. add one line to your CLAUDE.md so Claude reads it, for example: `before any risky action, read gated-actions.md`. the safety gate enforces the parts it can. this file covers the rest, the judgment calls a script cannot see.

**owner:** [your first name]
**last reviewed:** [date]. review it every 3 months, or whenever you connect a new account to Claude.

## what "gated" means

a gated action is one Claude never performs itself. Claude may prepare everything up to the act: write the email, build the page, draft the post, stage the command. then it stops, shows you exactly what it would do, and you either do it yourself or approve it in the moment.

drafting is never gated. sending is.

## the five gated classes

### 1. going live

- pushing code to GitHub or any remote: [your repos, e.g. "my-website"]
- deploying a website or app: [your host, e.g. "Squarespace, Vercel, Shopify"]
- publishing a product, page or listing: [e.g. "Gumroad product pages"]

### 2. public posts

- social accounts: [list them, e.g. "Instagram @yourbrand, LinkedIn"]
- communities, forums, groups: [e.g. "the local business Facebook group"]
- anything else public under your name: [e.g. "Google Business profile replies"]

### 3. messages to people

- email accounts: [e.g. "hello@yourbusiness"]
- texts, DMs, chat apps: [list]
- rule: any message to a client, lead, partner or friend. no exceptions for "just a quick reply".

### 4. money

- payment accounts: [e.g. "Stripe, PayPal"]
- anything that buys, upgrades, subscribes, refunds, invoices or tops up credits.
- ad spend of any size.

### 5. deleting

- deleting or overwriting files, folders, emails, calendar events, database rows, cloud documents.
- safer pattern: move to an `_archive` folder instead. archive is not gated.

## not gated (Claude may do these freely)

- reading anything in the business folder.
- writing drafts, notes, plans, memory notes and session handoffs.
- local, reversible work: [add yours, e.g. "creating new files in /drafts"]

## my own extra rules

- [e.g. "never contact anyone on the do-not-contact list in memory/clients.md"]
- [e.g. "never quote a price that is not in memory/offer-and-pricing.md"]
- [e.g. "never sign me up for anything"]

## when Claude hits a gate

1. stop. do not retry, reword, or find another route to the same result.
2. tell me in one line what you wanted to do and why.
3. show me the exact thing (the email text, the command, the amount).
4. wait for my answer.
