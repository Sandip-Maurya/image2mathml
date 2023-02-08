
import latex2mathml.converter
import re
def full_lat_converter(lat_str):
    
    # Mixed Function convert mixed content (latex+regular text) into mathml code
    def mixed_part(test_str):
        paralst = test_str.split('\n')
        fin_mathml = ''
        # divide the mixed part in each para
        for para in paralst:
            itr = re.finditer('\$.*?\$', para)
            fin_para = ''
            temp_ind = 0
            # find math_part and simultaneously convert it into mathmal and replace latexpart with it
            for match in itr:
                temp_txt = para[temp_ind:match.span()[0]]
                temp_math_ml = latex2mathml.converter.convert(match.group(0)[1:-1])
                fin_para += temp_txt + temp_math_ml
                temp_ind = match.span()[1]

            fin_para += para[temp_ind:]
            fin_para = '<p>' + fin_para + '</p>'
            fin_mathml += fin_para
            mixed_mathml = fin_mathml
        return mixed_mathml

    # Block Function returns mathml code for block latex code
    def block_part(test_str):

    # Array type latex converter function
        def arr_fun(test_str):

            test_str = test_str.replace('$$', '')
            test_str = test_str.replace('\n', '')

            if '\\left' in test_str:
                lft_ind = re.search(r'\\left', test_str).span()[1]
                arr_ind = re.search(r'\\begin', test_str).span()[0]
                if lft_ind < arr_ind:
                    return '<p>' + latex2mathml.converter.convert(test_str) + '</p>'

            test_str = re.sub(r'\\begin\{array\}\{.*?\}', '', test_str)
            test_str = re.sub(r'\\begin\{array\}', '', test_str)
            test_str = re.sub(r'\\end\{array\}', '', test_str)
            lst_lines = test_str.split('\\\\')
            lst_lines = ['<p>' + latex2mathml.converter.convert(i) + '</p>' for i in lst_lines]
            src_fin = ' '.join(lst_lines)

            return src_fin

        if r'\begin{array}' in test_str:
            block_mathml = arr_fun(test_str)
            
        elif r'\begin{aligned}' in test_str:
            
            test_str = test_str.replace('$$', '')
            test_str = test_str.replace('\n', '')
            test_str = test_str.replace('\\begin{aligned}', '')
            test_str = test_str.replace('\\end{aligned}', '')
            test_str = test_str.replace('&', '')
            lst_lines = test_str.split('\\\\')
            lst_lines = ['<p>' + latex2mathml.converter.convert(i) + '</p>' for i in lst_lines]
            src_fin = ' '.join(lst_lines)
            block_mathml = src_fin

        else:
            test_str1 = test_str.replace(r'$', '')
            block_mathml = '<p>' + latex2mathml.converter.convert(test_str1) + '</p>'

        return block_mathml

    # separating block latex and mixed latex code
    sep_itr = re.finditer(r'\$\$.*?\$\$', lat_str, re.DOTALL)
    mathml_fin = ''
    temp_ind = 0

    # Finding both type and converting them into mathml simultaneously.
    for match in sep_itr:
        mixed_mathml = mixed_part(lat_str[temp_ind:match.span()[0]])
        block_mathml = block_part(match.group(0))
        mathml_fin += mixed_mathml + block_mathml
        temp_ind = match.span()[1]

    mathml_fin += mixed_part(lat_str[temp_ind:])
    mathml_fin = mathml_fin.replace(r'<p></p>', '')
    
    return mathml_fin