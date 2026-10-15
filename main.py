import sys
import os
import asyncio

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
os.chdir(src_dir)

import game

async def main():
    await game.main()

if __name__ == '__main__':
    asyncio.run(main())
