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



## Tests:
<header>
    <div class="content">
        <h1>Coverage report:
            <span class="pc_cov">92%</span>
        </h1>
        <p class="text">
            <a class="nav" href="https://coverage.readthedocs.io">coverage.py v7.1.0</a>,
            created at 2023-01-26 15:31 +0100
        </p>
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
                <td class="name left"><a href="d_509fd8af0f7a1b49_admin_py.html">accounts/admin.py</a></td>
                <td>10</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="10 10">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_apps_py.html">accounts/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_forms_py.html">accounts/forms.py</a></td>
                <td>17</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="17 17">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_models_py.html">accounts/models.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_urls_py.html">accounts/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_509fd8af0f7a1b49_views_py.html">accounts/views.py</a></td>
                <td>135</td>
                <td>22</td>
                <td>0</td>
                <td class="right" data-ratio="113 135">84%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_admin_py.html">categories/admin.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_apps_py.html">categories/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_forms_py.html">categories/forms.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_models_py.html">categories/models.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_urls_py.html">categories/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_61e9babe6b460240_views_py.html">categories/views.py</a></td>
                <td>70</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="62 70">89%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_admin_py.html">counterparties/admin.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_apps_py.html">counterparties/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_forms_py.html">counterparties/forms.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_models_py.html">counterparties/models.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_urls_py.html">counterparties/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_cf6f0cb2358dab6d_views_py.html">counterparties/views.py</a></td>
                <td>70</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="62 70">89%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_a20243f409be1afc_admin_py.html">home/admin.py</a></td>
                <td>1</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="1 1">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_a20243f409be1afc_apps_py.html">home/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_a20243f409be1afc_models_py.html">home/models.py</a></td>
                <td>1</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="1 1">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_a20243f409be1afc_urls_py.html">home/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_a20243f409be1afc_views_py.html">home/views.py</a></td>
                <td>11</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="11 11">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_admin_py.html">plans/admin.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_apps_py.html">plans/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_forms_py.html">plans/forms.py</a></td>
                <td>6</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="6 6">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_models_py.html">plans/models.py</a></td>
                <td>13</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="13 13">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_urls_py.html">plans/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_f5e68ea9d835e894_views_py.html">plans/views.py</a></td>
                <td>86</td>
                <td>8</td>
                <td>0</td>
                <td class="right" data-ratio="78 86">91%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_admin_py.html">transactions/admin.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_apps_py.html">transactions/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_forms_py.html">transactions/forms.py</a></td>
                <td>10</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="10 10">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_models_py.html">transactions/models.py</a></td>
                <td>17</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="17 17">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_urls_py.html">transactions/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_242c59cbe7a704ec_views_py.html">transactions/views.py</a></td>
                <td>122</td>
                <td>10</td>
                <td>0</td>
                <td class="right" data-ratio="112 122">92%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_admin_py.html">wallets/admin.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_apps_py.html">wallets/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_forms_py.html">wallets/forms.py</a></td>
                <td>9</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="9 9">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_models_py.html">wallets/models.py</a></td>
                <td>10</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="10 10">100%</td>
            </tr>
            <tr class="file">
                <td class="name left"><a href="d_e7c17c6834bd7be8_urls_py.html">wallets/urls.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
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
                <td>806</td>
                <td>68</td>
                <td>0</td>
                <td class="right" data-ratio="738 806">92%</td>
            </tr>
        </tfoot>
    </table>
</main>
<footer>
    <div class="content">
        <p>
            <a class="nav" href="https://coverage.readthedocs.io">coverage.py v7.1.0</a>,
            created at 2023-01-26 15:31 +0100
        </p>
    </div>
</footer>




# How to run it locally:
1. Fork the repository
2. Clone the repository to your local machine, for example:
`git clone <your_repo_url>`
3. Create and activate virtual environment, for example for virtualenv:
`virtualenv -p python3.11 venv`
and then
`source venv/bin/activate`
4. In the main project folder (where manage.py is located), with virtual environment activated, use command:

`bash start.sh`

That will run the script, which does the following:
- installs required packages
- prepares and runs migrations (database file is created in main directory)
- flushes the database, in case script is run for the second time
- populates the database with starting data:
    - one user
    - one superuser
    - couple of instances of all necessary models
- tests code with pytest
- runs django development server, by default at http://127.0.0.1:8000/
- saves all the above info with details, passwords, test coverage, etc. to `log.txt` file in the main directory

### In case you run this script multiple times without killing the previous process, you'll get `port already in use` message

One easy way to free this port is:

`sudo lsof -t -i:8000`

or any other port number. This will output ID of the process that is running on this port,

for example `21987`, then

`sudo kill 21987`
