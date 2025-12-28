import Image from "next/image"

interface MenuItemProps {
  image: string;
  name: string;
  description: string;
}

export function MenuItem({ image, name, description }: MenuItemProps) {
  return (
    <div className="bg-gray-100 rounded-lg p-4 flex items-center">
      <div className="relative w-32 h-32 mr-4">
        <Image
          src={image}
          alt={name}
          fill
          className="object-cover rounded-md"
        />
      </div>
      <div>
        <h2 className="text-xl font-bold">{name}</h2>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}
