import re
PROMPTS={'v1':'Answer using only the supplied context. If evidence is missing, abstain.', 'v2':'Answer concisely using only context. Cite evidence. If missing, abstain.'}

def validate(output):
    issues=[]
    if not isinstance(output,dict): return {'passed':False,'issues':['Output must be JSON object']}
    for key in ('answer','citations','abstained'):
        if key not in output: issues.append('Missing '+key)
    if 'answer' in output and not isinstance(output['answer'],str): issues.append('answer must be string')
    if 'citations' in output and not isinstance(output['citations'],list): issues.append('citations must be list')
    if 'abstained' in output and not isinstance(output['abstained'],bool): issues.append('abstained must be boolean')
    if output.get('abstained') is False and not output.get('citations'): issues.append('Non-abstained answer requires citations')
    if re.search(r'ignore (all )?(previous|prior) instructions',str(output),re.I): issues.append('Potential injection echo')
    return {'passed':not issues,'issues':issues}

def evaluate(cases):
    results=[{'id':c['id'],**validate(c['output'])} for c in cases]
    return {'count':len(results),'pass_rate':round(sum(r['passed'] for r in results)/len(results),3) if results else 0,'cases':results}
