

from pathlib import Path
import yaml
import os

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text())

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys = False, allow_unicode=True)

def extract_text(vol_text):
    cur_vol_texts = {}
    for node_id, node in vol_text.items():
        for sub_node_id, sub_node in node['parts'].items():
            text = {}
            if sub_node['type'] == 'text' and sub_node['parts'] == {}:
                text[sub_node_id] = sub_node
                cur_vol_texts.update(text)
    return cur_vol_texts

def reconstruct_text(old_text, durchen_span):
    if 'ཚོགས་ཀྱི་བདག་པོའི་སྙིང་པོ།' in old_text['title']:
        print('cje')
    new_pg_end = int(old_text['pg_end']) - (int(old_text['img_loc_end']) - durchen_span['start'])
    durchen = {
        'title': f"{old_text['title']}བསྡུར་མཆན",
        'type': 'chapter',
        'img_loc_start': str(durchen_span['start']),
        'img_loc_end': str(durchen_span['end']),
        'pg_start': str(new_pg_end),
        'pg_end': str(old_text['pg_end']),
        'vol': old_text['vol'],
        'parts': {}
    }
    new_text = {
        'title': old_text['title'],
        'img_loc_start': str(old_text['img_loc_start']),
        'img_loc_end': str(durchen_span['start']),
        'pg_start': str(old_text['pg_start']),
        'pg_end': str(new_pg_end),
        'vol': old_text['vol'],
        'durchen': durchen 
    }
    return new_text

def reconstruct_vol_text(cur_vol_texts, durchens_span):
    new_vol_text = {}
    for (old_text_id, old_text), durchen_span in zip(cur_vol_texts.items(), durchens_span.values()):
        cur_text = {}
        new_text = reconstruct_text(old_text, durchen_span)
        cur_text[old_text_id] = new_text
        new_vol_text.update(cur_text)
    return new_vol_text

def flow():
    incomplete_texts = list(Path('./outline_fix/incomplete_text').iterdir())
    incomplete_texts.sort()
    durchen_spans = list(Path('./outline_fix/durchen_span').iterdir())
    durchen_spans.sort()
    for vol_incomplete_text, vol_durchen_span in zip(incomplete_texts[18:19], durchen_spans[18:19]):
        cur_vol_texts_yml = from_yaml(vol_incomplete_text)
        cur_vol_durchen_spans = from_yaml(vol_durchen_span)
        cur_vol_texts = extract_text(cur_vol_texts_yml)
        new_vol_text = reconstruct_vol_text(cur_vol_texts, cur_vol_durchen_spans)
        new_vol_text_yml = to_yaml(new_vol_text)
        Path(f'./complete_text/{vol_incomplete_text.stem}.yml').write_text(new_vol_text_yml, encoding='utf-8')
        print(f'{vol_incomplete_text.stem}and {vol_durchen_span} completed..')

if __name__ == "__main__":
    flow()

