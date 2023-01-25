# SaveIT - app for tracking personal finances
**Educational purposes only**
Live version available at:

https://marcinfraszczak.eu.pythonanywhere.com/

To see funcionalities, use credentials:  
username: 'Johny'  
password: 'Testpass123'  


## How to use app:

Main functionality depends on adding everyday expenses as 'transactions'.
Each transaction must have specified:
- date
- value
- counterparty (other side of transaction. for example name of the shop)
- category (like 'food', 'tickets', 'transportation' and so on)
- wallet that gathers transactions (usually one is enough, if you want to separate some transactions from another,you can do so by assigning them to another wallet)

Each item can be modified later, by clicking on its name in an item list view.
Dashboard view allows user to view graphs and summary for each month as well as summary for current wallet.

## Step by step instructions: 
1. Create an account, log in.
2. Add counterparties, cateogries, wallet. You are given one of each by default, but they are not enough.
3. Delete default values, if not needed anymore.
4. You can now add transactions.



Tests:
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="icon" sizes="32x32" href="favicon_32.png">
    <link rel="stylesheet" href="style.css" type="text/css">
</head>
<body class="indexfile">
<header>
    <div class="content">
        <h1>Coverage report:
            <span class="pc_cov">95%</span>
        </h1>
    </div>
</header>
<main id="index">
    <table class="index" data-sortable>
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left" aria-sort="none" data-shortcut="n">Module</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded</th>
                <th class="right" aria-sort="none" data-shortcut="c">coverage</th>
            </tr>
        </thead>
        <tbody>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_views_py.html">accounts/views.py</a></td>
                <td>135</td>
                <td>22</td>
                <td>0</td>
                <td class="right" data-ratio="113 135">84%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_views_py.html">categories/views.py</a></td>
                <td>70</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="62 70">89%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_views_py.html">counterparties/views.py</a></td>
                <td>70</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="62 70">89%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_views_py.html">plans/views.py</a></td>
                <td>86</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="78 86">91%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_views_py.html">transactions/views.py</a></td>
                <td>122</td>
                <td>10</td>
                <td>0</td>
                <td class="right" data-ratio="112 122">92%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_views_py.html">wallets/views.py</a></td>
                <td>108</td>
                <td>12</td>
                <td>0</td>
                <td class="right" data-ratio="96 108">89%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>1273</td>
                <td>68</td>
                <td>0</td>
                <td class="right" data-ratio="1205 1273">95%</td>
            </tr>
        </tfoot>
    </table>
    <p id="no_rows">
        No items found using the specified filter.
    </p>
        <p>49 files skipped due to complete coverage.</p>
</main>
<footer>
    <div class="content">
        <p>
            <a class="nav" href="https://coverage.readthedocs.io">coverage.py v7.1.0</a>,
            created at 2023-01-25 12:07 +0100
        </p>
    </div>
</footer>
</body>
</html>
