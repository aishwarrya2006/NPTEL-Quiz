import json
import re  

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    weeks = re.split(r'Week\s+(\d+)', content)
    
    questions = []
    
    # weeks[0] is empty or whitespace before first week
    for i in range(1, len(weeks), 2):
        week_num = int(weeks[i])
        week_content = weeks[i+1].strip()
        
        # Split by Q\d+:
        q_splits = re.split(r'Q\d+:', week_content)
        
        for q_block in q_splits[1:]:
            q_block = q_block.strip()
            if not q_block: continue
            
            # Extract question, options, answer
            # Format: Question text  A. option; B. option; C. option; D. option.  Ans: A. option.
            
            # Find the start of options: A. or True/False
            # Let's split by "  A. " or similar.
            
            # Actually, standard format seems to be:
            # Question text A. ...; B. ...; C. ...; D. ... Ans: ...
            
            # Find Ans:
            ans_split = re.split(r'Ans:', q_block)
            if len(ans_split) != 2:
                print(f"Error parsing Ans in: {q_block}")
                continue
                
            q_and_options = ans_split[0].strip()
            answer_raw = ans_split[1].strip()
            
            # Remove trailing dot from answer_raw if present
            if answer_raw.endswith('.'):
                answer_raw = answer_raw[:-1]
                
            # Find options
            # They usually start with A.
            opt_match = re.search(r'\s+A\.\s+(.*)', q_and_options)
            if opt_match:
                question_text = q_and_options[:opt_match.start()].strip()
                options_str = 'A. ' + opt_match.group(1)
                
                # Split options by ;
                # Wait, True/False has format: A. True; B. False.
                options_raw = re.split(r';\s*[A-D]\.\s+|\.\s*[A-D]\.\s+|^[A-D]\.\s+', options_str)
                # This might be tricky, let's just use regex to find all options
                opts = re.findall(r'[A-D]\.\s*(.*?)(?:;|$|\.(?=\s*[A-D]\.))', options_str)
                # Sometimes it ends with a dot.
                opts = [o.strip() for o in opts]
                if opts and opts[-1].endswith('.'):
                    opts[-1] = opts[-1][:-1]
            else:
                question_text = q_and_options
                opts = []

            # Clean answer: Extract just the text part if it starts with "A. "
            ans_text = answer_raw
            ans_match = re.match(r'[A-D]\.\s*(.*)', answer_raw)
            if ans_match:
                ans_text = ans_match.group(1).strip()
            
            # For exact matching, ensure answer matches one of the options
            best_match = ans_text
            for opt in opts:
                if ans_text.lower() in opt.lower() or opt.lower() in ans_text.lower():
                    best_match = opt
                    break

            questions.append({
                "week": week_num,
                "question": question_text,
                "options": opts,
                "answer": best_match
            })

    return questions

if __name__ == '__main__':
    data = parse_file('raw.txt')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Parsed {len(data)} questions.")
