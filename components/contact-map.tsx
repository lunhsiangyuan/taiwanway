export function ContactMap() {
  return (
    <section className="py-10">
      <div className="container px-4 md:px-6">
        <div className="w-full min-h-[400px] md:min-h-[600px] max-w-5xl mx-auto overflow-hidden rounded-lg shadow-lg">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2991.334411244905!2d-74.42462468255616!3d41.44520199999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c2cd0dff71cd7b%3A0xcafca35e649a39a2!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1706810757943!5m2!1sen!2sus"
            width="100%"
            height="100%"
            style={{ border: 0 }}
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          ></iframe>
        </div>
      </div>
    </section>
  )
}

