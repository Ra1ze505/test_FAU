import psutil

from src.apps.load.schemas import ResponseLoadSchema, CPULoadSchema, RAMLoadSchema, LoadSchema


class LoadService:

    async def get_all_usage(self) -> ResponseLoadSchema:
        cpu_load = await self._get_cpu_usage()
        ram_load = await self._get_ram_usage()
        return ResponseLoadSchema(cpu=CPULoadSchema(cpu_load=cpu_load),
                                  ram=RAMLoadSchema(ram_load=ram_load))

    async def get_any_load(self, data: LoadSchema):
        result = {}
        if 'cpu' in data.types:
            cpu_load = await self._get_cpu_usage()
            result['cpu'] = CPULoadSchema(cpu_load=cpu_load)

        if 'ram' in data.types:
            ram_load = await self._get_ram_usage()
            result['ram'] = RAMLoadSchema(ram_load=ram_load)

        return ResponseLoadSchema(**result)

    async def _get_cpu_usage(self) -> float:
        return psutil.cpu_percent(1)

    async def _get_ram_usage(self) -> float:
        return psutil.virtual_memory()[2]
