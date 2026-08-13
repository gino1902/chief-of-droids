# Requests

Four asks, four owners.

## 1. Role assignment for the access connector

Owner or User Access Administrator on `RG-DATABRICKS-DEV`. `mameyer@sqli.com`,
`mfouquet@sqli.com`.

> Can you run this? I get `AuthorizationFailed` on `roleAssignments/write`.
>
> ```bash
> az role assignment create \
>   --assignee bf9965b5-e9c1-4d43-8d3d-79b41e98ee3f \
>   --role "Storage Blob Data Contributor" \
>   --scope "/subscriptions/cbd4be67-d777-4841-bbf4-44d3c74d447d/resourceGroups/RG-DATABRICKS-DEV/providers/Microsoft.Storage/storageAccounts/stdbrmanagedfrasqlidev/blobServices/default/containers/managed"
> ```
>
> It is the managed identity of the access connector `ac-databricks-dev`. Unity
> Catalog needs this one role to read and write the container. Nothing else.
>
> Why it cannot be avoided: Databricks never reaches storage as the caller. It
> authenticates as the connector identity, so without this role every query fails
> for everyone, admins included.
>
> Better still, add me to `SGAP-RG-DATABRICKS-DEV` and I stop asking. Prod needs
> one of these per container.

## 2. OIDC federation policy

Databricks account admin, account `58bd71ac-c13e-40ea-80d3-cc4c79aee8f1`.

> Can you create an OIDC federation policy on service principal
> `SP-CICD-fra-sqli-dev`, app id `178e0409-b9d4-43f8-93c7-3b3e29ef0326`?
>
> - Issuer: `https://gitlab-paris.sqli.com`
> - Subject: `project_path:gmourgues/datawan:ref_type:branch:ref:main`
> - Audience: `https://adb-7405605180591006.6.azuredatabricks.net`
>
> Those three come straight out of the error Databricks returns today, and out of
> a real GitLab token. The subject pins to protected `main`, so no other branch
> can use the principal.
>
> Current failure: `invalid_grant`, `TOKEN_INVALID (Ensure a valid federation
> policy has been configured)`.

## 3. CI runner

Platform engineer.

> Can I get a Linux VM for a GitLab runner? Subscription
> `cbd4be67-d777-4841-bbf4-44d3c74d447d`, own resource group, two cores, Ubuntu,
> docker executor.
>
> - NAT gateway, static outbound IP, and send me the address.
> - Outbound 443 to `gitlab-paris.sqli.com` and
>   `adb-7405605180591006.6.azuredatabricks.net`. Both already reachable from
>   Azure, I tested from Cloud Shell.
> - `gitlab-runner` registered on the `datawan` project, untagged jobs enabled.
> - Tags `owner=sqli`, `environment=dev`, `cost_center=TBD`,
>   `project=databricks`.
> - In the Terraform please, not by hand.
>
> One runner for all environments is fine. Isolation comes from the service
> principals, not the machine.

## 4. SharePoint app registration

Entra admin, tenant `20f62116-4d0c-44ac-8a45-390ca2765601`.

> For the Databricks SharePoint connector I need an app registration with the
> Graph permissions it wants, admin consent, and a client secret. I mint the
> refresh token myself after that.
>
> Heads up: this one needs a secret. There is no federation option for it.

<!--
Version: 0.1 | Last Updated: 2026-08-13 | Status: Draft
-->
