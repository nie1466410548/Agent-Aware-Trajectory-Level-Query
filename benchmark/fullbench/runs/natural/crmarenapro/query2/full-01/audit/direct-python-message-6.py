import json
data = json.load(open('results/ef7835fce0104bb1a263cd6ce2dfd26c.json'))
titles = ['Volume-Based Discounts', 'TechPulse Solution Volume-Based Installation Timeline Policy', 'Product Quantity Limits', 'Mandatory Bundles for Quotes', 'Product Exclusion Constraints', 'Competing Offers']
for d in data:
    if d['title'].strip() in titles:
        print('='*80)
        print(d['id'], '|', d['title'])
        print(d['faq_answer__c'])
