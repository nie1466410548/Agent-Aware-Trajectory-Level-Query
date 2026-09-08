# Quote line items:
lines = [
    ("EcoPCB Creator", 3, 349.99, 0.0),
    ("AI Cirku-Tech", 2, 529.99, 0.0),
    ("DevVision IDE", 4, 299.99, 0.0),
    ("CollabDesign Studio", 35, 399.99, 15.0),
]
# Product Quantity Limits article: CollabDesign Studio max 25 per order
limits = {"AIOptics Vision":20,"CloudLink Designer":15,"CollabDesign Studio":25,"CryptGuard Module":10,
          "EduFlow Academy":5,"SecuManage Pro":30,"SecureAnalytics Pro":12,"IntegrGuard Secure":8,
          "CloudInnovate Space":18,"AI DesignShift":7}
for name, qty, price, disc in lines:
    total = qty*price*(1-disc/100)
    lim = limits.get(name)
    status = "VIOLATES qty limit" if (lim and qty > lim) else "ok"
    print(f"{name}: qty={qty}, unit={price}, disc={disc}%, total={total:.2f}, limit={lim} -> {status}")
# Volume-Based Discounts: 15% tier requires purchase over $20 -> total 11899.70 qualifies, discount ok
