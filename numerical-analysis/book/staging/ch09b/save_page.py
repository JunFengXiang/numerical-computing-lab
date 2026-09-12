from pathlib import Path
SOURCE_HASH='0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
BASE=Path(__file__).resolve().parent

def save(n,body):
    head=f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n}.jpeg\nsource_sha256: {SOURCE_HASH}\nstatus: agent_reviewed_transcription\n---\n\n[原页](../../../source-images/pdf-{n}.jpeg)\n\n<!-- source-page: {n} -->\n\n'
    (BASE/'pages'/f'pdf-{n}.md').write_text(head+body.strip()+'\n')
