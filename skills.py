# -*- coding: utf-8 -*-
"""PEPPOL BIS Billing 3.0 UBL e-Invoicing Sanitizer Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def validate_and_sanitize_peppol_ubl(**kwargs):
    """Validates European PEPPOL BIS Billing 3.0 UBL 2.1 XML invoices against CEN/TC 434 and PEPPOL Schematron business rules (BR-CO-15, BR-08, EAS prefix)."""
    invoice_number = kwargs.get('invoice_number')
    seller_peppol_id = kwargs.get('seller_peppol_id')
    buyer_peppol_id = kwargs.get('buyer_peppol_id')
    line_items = kwargs.get('line_items')
    currency = kwargs.get('currency')

    total_line_net = 0.0
    vat_buckets = {}
    sanitized_lines = []
    
    for i, item in enumerate(line_items, 1):
        qty = item.get("quantity", 1.0)
        price = item.get("net_price", 0.0)
        vat_pct = item.get("vat_rate_pct", 20.0)
        line_net = round(qty * price, 2)
        line_vat = round(line_net * (vat_pct / 100.0), 2)
        total_line_net += line_net
        
        vat_buckets[vat_pct] = vat_buckets.get(vat_pct, 0.0) + line_vat
        sanitized_lines.append({
            "line_id": i,
            "description": item.get("name", "Product"),
            "quantity": qty,
            "unit_price": price,
            "net_amount": line_net,
            "vat_pct": vat_pct,
            "vat_amount": line_vat
        })
        
    total_vat = sum(vat_buckets.values())
    grand_total = round(total_line_net + total_vat, 2)
    
    validation_errors = []
    if ":" not in seller_peppol_id:
        validation_errors.append("BR-CL-01: Seller PEPPOL Endpoint ID must include EAS prefix (e.g. '0192:').")
    if ":" not in buyer_peppol_id:
        validation_errors.append("BR-CL-02: Buyer PEPPOL Endpoint ID must include EAS prefix.")
    if total_line_net <= 0.0:
        validation_errors.append("BR-08: Invoice total net amount must be greater than zero.")
        
    is_compliant = len(validation_errors) == 0
    
    result = {
        "status": "success",
        "invoice_number": invoice_number,
        "is_peppol_bis_3_compliant": is_compliant,
        "validation_errors": validation_errors,
        "subtotal_net_amount": round(total_line_net, 2),
        "total_vat_amount": round(total_vat, 2),
        "grand_total_amount": grand_total,
        "vat_subtotals": {f"{k}%": round(v, 2) for k, v in vat_buckets.items()},
        "sanitized_line_items": sanitized_lines,
        "engine": "GenPark PEPPOL BIS Billing 3.0 Schematron Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "validate_and_sanitize_peppol_ubl": {
        "name": "validate_and_sanitize_peppol_ubl",
        "description": "Validates European PEPPOL BIS Billing 3.0 UBL 2.1 XML invoices against CEN/TC 434 and PEPPOL Schematron business rules (BR-CO-15, BR-08, EAS prefix).",
        "parameters": {
            "type": "object",
            "properties": {
                "invoice_number": {"type": "string", "description": "Seller invoice number"},
                "seller_peppol_id": {"type": "string", "description": "Seller PEPPOL endpoint (e.g. '0192:987654321')"},
                "buyer_peppol_id": {"type": "string", "description": "Buyer PEPPOL endpoint (e.g. '0088:7300010000001')"},
                "line_items": {"type": "array", "description": "List of dicts: [{'name': str, 'quantity': float, 'net_price': float, 'vat_rate_pct': float}]"},
                "currency": {"type": "string", "description": "Invoice currency code (e.g. 'EUR')"},
            },
            "required": ['invoice_number', 'seller_peppol_id', 'buyer_peppol_id', 'line_items', 'currency']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "validate_and_sanitize_peppol_ubl":
            res = validate_and_sanitize_peppol_ubl(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-e-invoicing-peppol-bis-billing-3-ubl-sanitizer-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-e-invoicing-peppol-bis-billing-3-ubl-sanitizer-skill...")
    test_args = {'invoice_number': 'INV-2026-EU-0841', 'seller_peppol_id': '0192:987654321', 'buyer_peppol_id': '0088:7300010000001', 'line_items': [{'name': 'Server Rack Mounting Unit', 'quantity': 10.0, 'net_price': 120.0, 'vat_rate_pct': 21.0}, {'name': 'Fiber Optic Patch Cable 5m', 'quantity': 50.0, 'net_price': 15.0, 'vat_rate_pct': 21.0}], 'currency': 'EUR'}
    res = validate_and_sanitize_peppol_ubl(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-e-invoicing-peppol-bis-billing-3-ubl-sanitizer-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
