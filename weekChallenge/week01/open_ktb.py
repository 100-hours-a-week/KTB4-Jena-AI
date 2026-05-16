import argparse
import webbrowser

WEBSITE = {
    'qr': 'https://kakao-tech-bootcamp.goorm.io/learn/lecture/64676/%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%85%8C%ED%81%AC-%EB%B6%80%ED%8A%B8%EC%BA%A0%ED%94%84-ai-%EC%8B%A4%EB%AC%B4-%EA%B0%9C%EB%B0%9C-%EA%B3%BC%EC%A0%95-4%EA%B8%B0',
    'zep': 'https://zep.us/play/8lj15q',
    'zoom': 'https://app.zoom.us/wc/88542079125/join?ref_from=launch&pwd=mpWG24Ato1plo3jlLYBHQFD9Gyu5St.1&_x_zm_rtaid=BQw6Y-UiTKCq_wXudvJGiA.1778716312693.7897212bfa1aab8a58c1ec1813cbac41&_x_zm_rhtaid=185&fromPWA=1',
    'notion': 'https://www.notion.so/adapterz/KTB-4-AI-34f394a480618081a559d2b16ea902e1',
    'git': 'https://github.com/100-hours-a-week'
}

def open_ktb(args):
    # Open default websites
    webbrowser.open(WEBSITE['qr'])
    webbrowser.open(WEBSITE['zep'])
    webbrowser.open(WEBSITE['zoom'])

    num = len(args.sites) + 3
    print(f"Kakao Bootcamp {num} website is opening ...")

    for site in args.sites:
        if site in WEBSITE:
            webbrowser.open(WEBSITE[site])


parser = argparse.ArgumentParser(description='Opening Kakao Bootcamp related website CLI.')
subparser = parser.add_subparsers(dest='command')

ktb_parser = subparser.add_parser('open_ktb', help='Open ktb website')
ktb_parser.add_argument("sites", nargs="*")

ktb_parser.set_defaults(func=open_ktb)
args = parser.parse_args()

if args.command:
    args.func(args)