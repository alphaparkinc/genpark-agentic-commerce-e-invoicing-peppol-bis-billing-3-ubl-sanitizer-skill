# PEPPOL BIS Billing 3.0 UBL e-Invoicing Sanitizer Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `validate_and_sanitize_peppol_ubl`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Validates European PEPPOL BIS Billing 3.0 UBL 2.1 XML invoices against CEN/TC 434 and PEPPOL Schematron business rules (BR-CO-15, BR-08, EAS prefix).

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (e-Invoicing / Tax Compliance)`

## MCP Tool Specification
### `validate_and_sanitize_peppol_ubl`
Parameters:
- `invoice_number` (str): Seller invoice number
- `seller_peppol_id` (str): Seller PEPPOL endpoint (e.g. '0192:987654321')
- `buyer_peppol_id` (str): Buyer PEPPOL endpoint (e.g. '0088:7300010000001')
- `line_items` (list): List of dicts: [{'name': str, 'quantity': float, 'net_price': float, 'vat_rate_pct': float}]
- `currency` (str): Invoice currency code (e.g. 'EUR')

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-e-invoicing-peppol-bis-billing-3-ubl-sanitizer-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-e-invoicing-peppol-bis-billing-3-ubl-sanitizer-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
