import yaml


from pathlib import Path


def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys = False, allow_unicode=True)

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding='utf-8'))

def reconstruct_text(text_id, text, title):
    if text_id == 'O1PD1123714CZ89847':
        print(title)
    cur_text[text_id] = {
        'pedurma_title': text['title'],
        'text_title': title[1],
        'rkts_id': title[0],
        'img_loc_start': text['img_loc_start'],
        'img_loc_end': text['img_loc_end'],
        'pg_start': text['pg_start'],
        'pg_end': text['pg_end'],
        'vol': text['vol'],
        'durchen': text['durchen'],    
    }
    return cur_text

if __name__ == "__main__":
    old_outline = from_yaml(Path('./outline_fix/kangyur_text_durchen.yml'))
    pedurma_text_titles = from_yaml(Path('./outline_fix/pedurma_text_title.yml'))
    new_outline = {}
    for (text_id, text), title in zip(old_outline.items(), pedurma_text_titles):
        cur_text = {}
        cur_text = reconstruct_text(text_id, text, title)
        new_outline.update(cur_text)
    new_outline_yml = to_yaml(new_outline)
    Path('./outline_fix/new_pedurma_outline.yml').write_text(new_outline_yml, encoding='utf-8')
    len(pedurma_text_titles)

