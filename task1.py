import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
import argparse
from time import time

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", required=True, help="Source folder")
parser.add_argument("--output", "-o", default="dist", help="Output folder")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")


async def read_folder(path: AsyncPath) -> None:
    async for el in path.iterdir():
        if await el.is_dir():
            await read_folder(el)
        else:
            await copy_file(el)


async def copy_file(file: AsyncPath) -> None:
    ext = file.suffix.lower().strip('.')
    new_path = AsyncPath(output) / ext
    await new_path.mkdir(exist_ok=True, parents=True)
    await copyfile(file, new_path / file.name)


async def main():
    start = time()

    task = asyncio.create_task(read_folder(AsyncPath(source)))

    try:
        await task
    except Exception as e:
        print(f"Виняток під час виконання завдання: {e}")
    else:
        print(f"Завдання завершилося успішно")
        print(f"Час виконання: {time() - start}")

if __name__ == '__main__':
    asyncio.run(main())
