interface MenuItemProps {
  image: string;
  name: string;
  description: string;
}

export function MenuItem({ image, name, description }: MenuItemProps) {
  return (
    <div className="bg-gray-100 rounded-lg p-4 flex items-center">
      <img src={image} alt={name} className="w-32 h-32 object-cover rounded-md mr-4" />
      <div>
        <h2 className="text-xl font-bold">{name}</h2>
        <p className="text-gray-600">{description}</p>
      </div>
    </div>
  );
}
